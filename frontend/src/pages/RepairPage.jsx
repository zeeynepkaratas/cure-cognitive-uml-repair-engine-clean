import { useState, useEffect, useRef } from 'react';
import {
  Play, CheckCircle, XCircle, Download, RotateCcw,
  Wrench, Home, BarChart2, AlertCircle, Clock, Cpu,
} from 'lucide-react';
import { autonomousRepair } from '../services/api';
import { downloadPuml, downloadSvg, formatDuration } from '../utils';
import Alert from '../components/Alert';

// ── Faz sabitleri (artık mockData'ya bağımlı değil) ──────────────────────────
const PHASES = [
  { key: 'ANALIZ',         label: 'Analiz',        desc: 'OCL kuralları ile diyagram taranıyor' },
  { key: 'ONARIM',         label: 'Onarım',         desc: 'AI Healer ajanı düzeltmeleri uyguluyor' },
  { key: 'DERLEME_TESTI',  label: 'Derleme Testi',  desc: 'Compile testi çalıştırılıyor' },
  { key: 'TAMAMLANDI',     label: 'Tamamlandı',     desc: 'İterasyon sonuçlandı' },
];

// ── Progress çubuğu ───────────────────────────────────────────────────────────
const RepairProgress = ({ phases, activePhaseIndex, success, failed }) => (
  <div className="repair-progress">
    <div className="repair-progress__steps">
      {phases.map((phase, idx) => {
        const isDone = idx < activePhaseIndex || success || failed;
        const isActive = idx === activePhaseIndex && !success && !failed;
        return (
          <div
            key={phase.key}
            className={`repair-step ${isDone ? 'repair-step--done' : ''} ${isActive ? 'repair-step--active' : ''} ${(!isDone && !isActive) ? 'repair-step--pending' : ''}`}
          >
            <div className="repair-step__icon">
              {isDone
                ? <CheckCircle size={18} />
                : isActive
                  ? <div className="spinner spinner--sm" />
                  : <div className="repair-step__circle" />
              }
            </div>
            <div className="repair-step__info">
              <span className="repair-step__label">{phase.label}</span>
              <span className="repair-step__desc">{phase.desc}</span>
            </div>
            {idx < phases.length - 1 && (
              <div className={`repair-step__connector ${isDone ? 'repair-step__connector--done' : ''}`} />
            )}
          </div>
        );
      })}
    </div>
  </div>
);

// ── İterasyon kartı (API formatı) ─────────────────────────────────────────────
const IterCard = ({ iter, isLatest }) => {
  const [open, setOpen] = useState(isLatest);

  // Backend'in döndürdüğü iterasyon yapısına göre alan isimleri:
  const no = iter.iteration_no ?? iter.iterasyon_no ?? '?';
  const compileOk = iter.compile_result?.basarili ?? (iter.status === 'AI_HEALER_APPLIED' || iter.status === 'COMPILE_OK');
  const fixSummary = iter.fix_summary ?? iter.duzeltme_ozeti ?? null;
  const compileErrors = iter.compile_result?.syntax?.hatalar ?? iter.compile_result?.ocl?.hatalar ?? [];
  const ocl = iter.compile_result?.ocl ?? null;

  return (
    <div className={`iteration-card ${compileOk ? 'iteration-card--success' : 'iteration-card--failed'} ${isLatest ? 'iteration-card--latest' : ''}`}>
      <button className="iteration-card__header" onClick={() => setOpen(v => !v)} aria-expanded={open}>
        <div className="iteration-card__number">
          {compileOk
            ? <CheckCircle size={20} className="icon-success" />
            : <XCircle size={20} className="icon-failed" />
          }
          <span>Deneme {no}</span>
          {isLatest && <span className="iteration-card__latest-badge">Son</span>}
        </div>
        <div className="iteration-card__meta">
          <span className={compileOk ? 'compile-ok' : 'compile-fail'}>
            Derleme: {compileOk ? 'Başarılı' : 'Başarısız'}
          </span>
          {ocl && (
            <span className="iteration-card__score">
              OCL Skor: {ocl.yuzde ?? Math.round((ocl.skor ?? 0) * 100)}%
            </span>
          )}
        </div>
        <span className="iteration-card__toggle">
          {open ? '▲' : '▼'}
        </span>
      </button>

      {open && (
        <div className="iteration-card__body">
          <p className="iteration-card__status-label">
            Durum: <code>{iter.status}</code>
          </p>
          {fixSummary && (
            <div className="iteration-section">
              <div className="iteration-section__title"><Wrench size={13} /> Düzeltme Özeti</div>
              <p className="iteration-fix-summary">{fixSummary}</p>
            </div>
          )}
          {compileErrors.length > 0 && (
            <div className="iteration-section">
              <div className="iteration-section__title"><AlertCircle size={13} /> Derleme Hataları</div>
              {compileErrors.map((e, i) => (
                <div key={i} className="iteration-compile-error">
                  <XCircle size={13} />
                  <span>{typeof e === 'string' ? e : (e.mesaj ?? JSON.stringify(e))}</span>
                </div>
              ))}
            </div>
          )}
          {compileOk && !compileErrors.length && (
            <div className="iteration-compile-success">
              <CheckCircle size={13} />
              <span>Derleme testi geçti — bu iterasyon onaylandı.</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ── Ana RepairPage ─────────────────────────────────────────────────────────────

const RepairPage = ({ data, onNavigate }) => {
  const [status, setStatus] = useState('idle'); // idle | loading | success | failed
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [activePhase, setActivePhase] = useState(0);
  const phaseRef = useRef(null);
  const [toast, setToast] = useState('');

  // Sayfa açıldığında ve geçerli veri varsa otomatik başlat
  useEffect(() => {
    if (data?.plantuml_kodu && status === 'idle') {
      handleStart();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 2500);
  };

  const handleStart = async () => {
    if (!data?.plantuml_kodu) {
      setError('Onarım başlatmak için önce analiz yapın ve buraya yönlendirin.');
      return;
    }

    setStatus('loading');
    setResult(null);
    setError('');
    setActivePhase(0);

    // Faz animasyonu simüle et (API çağrısı devam ederken)
    let phaseIdx = 0;
    phaseRef.current = setInterval(() => {
      phaseIdx = Math.min(phaseIdx + 1, PHASES.length - 2); // Son faza API bittikten sonra geç
      setActivePhase(phaseIdx);
    }, 3000);

    try {
      const res = await autonomousRepair(
        data.plantuml_kodu,
        data.srs_metni ?? null,
        3
      );

      clearInterval(phaseRef.current);
      setActivePhase(PHASES.length - 1);
      setResult(res);
      setStatus(res.basarili ? 'success' : 'failed');
    } catch (err) {
      clearInterval(phaseRef.current);
      setError(typeof err === 'string' ? err : 'Onarım sırasında beklenmedik bir hata oluştu.');
      setStatus('failed');
    }
  };

  const handleReset = () => {
    setStatus('idle');
    setResult(null);
    setError('');
    setActivePhase(0);
    clearInterval(phaseRef.current);
  };

  const iterasyonlar = result?.iterasyonlar ?? [];
  const finalUml = result?.final_plantuml ?? data?.plantuml_kodu ?? '';
  const finalSvg = result?.final_render?.svg ?? null;
  const semantik = result?.semantik ?? null;

  return (
    <div className="page repair-page">
      <div className="container">
        {toast && (
          <div className="toast-notification">
            <CheckCircle size={15} />
            {toast}
          </div>
        )}

        {/* Üst başlık */}
        <div className="results-header">
          <div className="results-header__left">
            <button className="back-btn" onClick={() => onNavigate('results', data?.sourceData)}>
              <BarChart2 size={15} />
              <span>Sonuçlara Dön</span>
            </button>
            <div className="results-title-block">
              <h2 className="results-title">Otonom Onarım</h2>
              <div className="results-meta">
                {data?.document_name && <span className="results-meta__item">📄 {data.document_name}</span>}
                {result?.sure_saniye && <span className="results-meta__item">⏱ {result.sure_saniye}s</span>}
                {result?.sla_gecti_mi !== undefined && (
                  <span className={`results-meta__item ${result.sla_gecti_mi ? 'meta-ok' : 'meta-warn'}`}>
                    {result.sla_gecti_mi ? '✓ SLA Geçti' : '⚠ SLA Aşıldı'}
                  </span>
                )}
              </div>
            </div>
          </div>

          {status === 'success' && (
            <div className="results-header__actions">
              {finalSvg && (
                <button className="btn-icon" onClick={() => { downloadSvg(finalSvg, 'repaired.svg'); showToast('SVG indirildi.'); }}>
                  <Download size={16} /> <span>SVG</span>
                </button>
              )}
              <button className="btn-icon" onClick={() => { downloadPuml(finalUml, 'repaired.puml'); showToast('PlantUML indirildi.'); }}>
                <Download size={16} /> <span>PlantUML</span>
              </button>
            </div>
          )}
        </div>

        {/* Veri eksik uyarısı */}
        {!data?.plantuml_kodu && (
          <div className="empty-results">
            <Cpu size={64} className="empty-results__icon" />
            <h2>Onarım için veri bulunamadı</h2>
            <p>Lütfen önce Ana Sayfa'dan bir SRS belgesi yükleyip analiz yapın, ardından "Onarıma Gönder" butonuna tıklayın.</p>
            <button className="btn btn-primary" onClick={() => onNavigate('home')}>
              <Home size={18} /> <span>Ana Sayfaya Git</span>
            </button>
          </div>
        )}

        {/* Durum banner */}
        {data?.plantuml_kodu && (
          <>
            {status === 'idle' && (
              <div className="repair-banner repair-banner--waiting">
                <div className="pulse-dot" />
                <div className="repair-banner__text">
                  <strong>Hazır — Onarımı başlatmak için butona tıklayın.</strong>
                  <span>Sistem AI ajanı ile UML diyagramını analiz edip otomatik onarım uygulayacak.</span>
                </div>
              </div>
            )}
            {status === 'loading' && (
              <div className="repair-banner repair-banner--waiting">
                <div className="pulse-dot" />
                <div className="repair-banner__text">
                  <strong>Otonom onarım çalışıyor…</strong>
                  <span>AI ajanı diyagramı analiz edip düzeltmeler uyguluyor. Bu işlem 10-30 saniye sürebilir.</span>
                </div>
              </div>
            )}
            {status === 'success' && (
              <div className="repair-banner repair-banner--success">
                <CheckCircle size={24} />
                <div className="repair-banner__text">
                  <strong>Onarım Başarıyla Tamamlandı</strong>
                  <span>
                    {iterasyonlar.length} iterasyon uygulandı.
                    {result?.sure_saniye && ` Toplam süre: ${result.sure_saniye}s.`}
                    {' '}Final diyagramı aşağıdan indirebilirsiniz.
                  </span>
                </div>
              </div>
            )}
            {status === 'failed' && (
              <div className="repair-banner repair-banner--failed">
                <XCircle size={24} />
                <div className="repair-banner__text">
                  <strong>Onarım Tamamlanamadı</strong>
                  <span>
                    {iterasyonlar.length > 0
                      ? `${iterasyonlar.length} iterasyon denendi ancak hatalar giderilemedi.`
                      : 'API hatası nedeniyle onarım başlatılamadı.'}
                    {' '}Lütfen SRS belgesini güncelleyip tekrar deneyin.
                  </span>
                </div>
              </div>
            )}

            {error && <Alert type="error" message={error} onClose={() => setError('')} />}

            {/* Progress (loading sırasında) */}
            {status === 'loading' && (
              <RepairProgress
                phases={PHASES}
                activePhaseIndex={activePhase}
                success={false}
                failed={false}
              />
            )}
            {(status === 'success' || status === 'failed') && (
              <RepairProgress
                phases={PHASES}
                activePhaseIndex={PHASES.length}
                success={status === 'success'}
                failed={status === 'failed'}
              />
            )}

            {/* Aksiyon butonları */}
            <div className="repair-actions">
              {status === 'idle' && (
                <button className="btn btn-primary" onClick={handleStart}>
                  <Play size={18} />
                  <span>Onarımı Başlat</span>
                </button>
              )}
              {status === 'loading' && (
                <button className="btn btn-secondary" disabled>
                  <div className="spinner spinner--sm" />
                  <span>Onarım devam ediyor…</span>
                </button>
              )}
              {(status === 'success' || status === 'failed') && (
                <div className="repair-done-actions">
                  <button className="btn btn-outline" onClick={handleReset}>
                    <RotateCcw size={16} />
                    <span>Tekrar Dene</span>
                  </button>
                  {status === 'success' && finalSvg && (
                    <button className="btn btn-primary" onClick={() => { downloadSvg(finalSvg, 'repaired.svg'); showToast('İndirildi.'); }}>
                      <Download size={16} />
                      <span>Final Diyagramı İndir</span>
                    </button>
                  )}
                </div>
              )}
            </div>

            {/* İterasyon timeline */}
            {iterasyonlar.length > 0 && (
              <div className="repair-timeline">
                <div className="repair-timeline__header">
                  <Clock size={18} />
                  <span>İterasyon Zaman Çizelgesi</span>
                  <span className="repair-timeline__count">{iterasyonlar.length} deneme</span>
                </div>
                <div className="repair-timeline__list">
                  {iterasyonlar.map((iter, idx) => (
                    <div key={idx} className="repair-timeline__item">
                      <div className="repair-timeline__line-wrap">
                        <div className={`repair-timeline__dot ${
                          iter.compile_result?.basarili ? 'repair-timeline__dot--success' : 'repair-timeline__dot--failed'
                        }`} />
                        {idx < iterasyonlar.length - 1 && <div className="repair-timeline__connector" />}
                      </div>
                      <div className="repair-timeline__card">
                        <IterCard iter={iter} isLatest={idx === iterasyonlar.length - 1} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Final UML (başarılıysa) */}
            {status === 'success' && finalUml && (
              <div className="content-card final-uml-card">
                <div className="card-header" style={{ textAlign: 'left', marginBottom: 20 }}>
                  <h3 style={{ fontSize: 22 }}>Final PlantUML</h3>
                </div>
                {finalSvg && (
                  <div className="svg-viewer" style={{ marginBottom: 24 }}>
                    <div dangerouslySetInnerHTML={{ __html: finalSvg }} />
                  </div>
                )}
                <div className="code-viewer">
                  <div className="code-viewer__toolbar">
                    <span className="code-viewer__lang">PlantUML</span>
                  </div>
                  <pre className="code-viewer__code">{finalUml}</pre>
                </div>
              </div>
            )}

            {/* Semantik sonuç (varsa) */}
            {semantik && status === 'success' && (
              <div className="content-card" style={{ marginTop: 24 }}>
                <div className="card-header" style={{ textAlign: 'left', marginBottom: 16 }}>
                  <h3 style={{ fontSize: 20 }}>Semantik Değerlendirme (Onarım Sonrası)</h3>
                </div>
                <div className="repair-semantik">
                  <div className="repair-semantik__score">
                    <span>Semantik Skoru</span>
                    <strong style={{ color: semantik.gecti_mi ? 'var(--success)' : 'var(--warning)' }}>
                      {semantik.yuzde ?? Math.round((semantik.genel_skor ?? 0) * 100)}%
                    </strong>
                    <span className={semantik.gecti_mi ? 'meta-ok' : 'meta-warn'}>
                      {semantik.gecti_mi ? '✓ Eşiği Geçti' : '⚠ Eşik Altı'}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default RepairPage;
