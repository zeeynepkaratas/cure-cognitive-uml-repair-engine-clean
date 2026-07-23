import { useState } from 'react';
import {
  CheckCircle, XCircle, AlertTriangle, AlertCircle,
  Copy, Download, Wrench, Code2, Eye, EyeOff,
  ArrowRight, Home, BarChart2, ChevronDown, ChevronUp,
  Info, BookOpen, Layers,
} from 'lucide-react';
import { copyToClipboard, downloadPuml, downloadSvg, formatTimestamp, scoreColor } from '../utils';
import Alert from '../components/Alert';

// ── Yardımcı bileşenler ───────────────────────────────────────────────────────

const ScoreRing = ({ percent, label, size = 100 }) => {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const dash = ((percent ?? 0) / 100) * circ;
  const color = scoreColor(percent ?? 0);

  return (
    <div className="score-ring" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="var(--border)" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
          style={{ transition: 'stroke-dasharray 1s ease' }}
        />
      </svg>
      <div className="score-ring__text">
        <span className="score-ring__value" style={{ color }}>{percent ?? '—'}%</span>
        <span className="score-ring__label">{label}</span>
      </div>
    </div>
  );
};

const CopyButton = ({ text, small }) => {
  const [copied, setCopied] = useState(false);
  const handle = async () => {
    await copyToClipboard(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button className={`copy-btn ${small ? 'copy-btn--sm' : ''}`} onClick={handle} title="Kopyala">
      {copied ? <CheckCircle size={small ? 13 : 15} /> : <Copy size={small ? 13 : 15} />}
      {!small && <span>{copied ? 'Kopyalandı!' : 'Kopyala'}</span>}
    </button>
  );
};

const CollapsibleSection = ({ title, icon: Icon, count, children, defaultOpen = true, badge }) => {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="collapsible-section">
      <button className="collapsible-section__header" onClick={() => setOpen(v => !v)}>
        <span className="collapsible-section__title">
          <Icon size={18} />
          {title}
          {count !== undefined && <span className="collapsible-section__count">{count}</span>}
          {badge && <span className="collapsible-section__badge">{badge}</span>}
        </span>
        {open ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>
      {open && <div className="collapsible-section__body">{children}</div>}
    </div>
  );
};

// ── OCL Sonuç Paneli ─────────────────────────────────────────────────────────

const OclPanel = ({ ocl }) => {
  if (!ocl) return null;
  const percent = ocl.yuzde ?? Math.round((ocl.skor ?? 0) * 100);
  const hasErrors = (ocl.hatalar ?? []).length > 0;
  const hasWarnings = (ocl.uyarilar ?? []).length > 0;

  return (
    <div className={`ocl-panel ${ocl.gecerli_mi ? 'ocl-panel--valid' : 'ocl-panel--invalid'}`}>
      <div className="ocl-panel__header">
        <div className="ocl-panel__status">
          {ocl.gecerli_mi
            ? <><CheckCircle size={20} className="icon-success" /> <span>OCL Geçti</span></>
            : <><XCircle size={20} className="icon-failed" /> <span>OCL Başarısız</span></>
          }
        </div>
        <div className="ocl-panel__score">
          <span className="ocl-score-bar-label">Skor</span>
          <div className="ocl-score-bar-wrap">
            <div
              className="ocl-score-bar"
              style={{ width: `${percent}%`, background: scoreColor(percent) }}
            />
          </div>
          <span className="ocl-score-pct" style={{ color: scoreColor(percent) }}>{percent}%</span>
        </div>
      </div>

      {hasErrors && (
        <div className="ocl-list ocl-list--errors">
          <p className="ocl-list__title"><AlertCircle size={14} /> Hatalar ({ocl.hatalar.length})</p>
          {ocl.hatalar.map((h, i) => (
            <div key={i} className="ocl-item ocl-item--error">
              <AlertCircle size={13} />
              <span>{typeof h === 'string' ? h : (h.mesaj || JSON.stringify(h))}</span>
            </div>
          ))}
        </div>
      )}

      {hasWarnings && (
        <div className="ocl-list ocl-list--warnings">
          <p className="ocl-list__title"><AlertTriangle size={14} /> Uyarılar ({ocl.uyarilar.length})</p>
          {ocl.uyarilar.map((u, i) => (
            <div key={i} className="ocl-item ocl-item--warning">
              <AlertTriangle size={13} />
              <span>{typeof u === 'string' ? u : (u.mesaj || JSON.stringify(u))}</span>
            </div>
          ))}
        </div>
      )}

      {!hasErrors && !hasWarnings && (
        <p className="ocl-clean">Tüm OCL kuralları geçti. Hata veya uyarı bulunamadı.</p>
      )}
    </div>
  );
};

// ── Semantik Panel ───────────────────────────────────────────────────────────

const SemanticPanel = ({ semantik }) => {
  if (!semantik) return null;
  const percent = semantik.yuzde ?? Math.round((semantik.genel_skor ?? 0) * 100);
  const halucinasyonlar = semantik.halusinasyonlar ?? [];
  const eksikSiniflar = semantik.eksik_siniflar ?? [];
  const ieee = semantik.ieee_kriterleri ?? {};

  return (
    <div className={`semantic-panel ${semantik.gecti_mi ? 'semantic-panel--pass' : 'semantic-panel--fail'}`}>
      <div className="semantic-panel__header">
        <div className="semantic-panel__status">
          {semantik.gecti_mi
            ? <><CheckCircle size={20} className="icon-success" /> <span>Semantik Geçti</span></>
            : <><XCircle size={20} className="icon-failed" /> <span>Semantik Düşük</span></>
          }
        </div>
        <ScoreRing percent={percent} label="Sadakat" size={90} />
      </div>

      {/* IEEE Kriterleri */}
      {Object.keys(ieee).length > 0 && (
        <div className="ieee-grid">
          {Object.entries(ieee).map(([key, val]) => {
            const pct = typeof val === 'number' ? Math.round(val * 100) : (val?.skor ? Math.round(val.skor * 100) : null);
            return (
              <div key={key} className="ieee-item">
                <span className="ieee-item__key">{key}</span>
                {pct !== null && (
                  <div className="ieee-item__bar-wrap">
                    <div className="ieee-item__bar" style={{ width: `${pct}%`, background: scoreColor(pct) }} />
                  </div>
                )}
                <span className="ieee-item__pct" style={pct !== null ? { color: scoreColor(pct) } : {}}>
                  {pct !== null ? `${pct}%` : (typeof val === 'boolean' ? (val ? '✓' : '✗') : String(val))}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {halucinasyonlar.length > 0 && (
        <div className="semantic-list">
          <p className="semantic-list__title"><AlertTriangle size={14} /> Halüsinasyonlar ({halucinasyonlar.length})</p>
          {halucinasyonlar.map((h, i) => (
            <div key={i} className="semantic-item semantic-item--hallucination">
              <AlertTriangle size={13} />
              <span>{typeof h === 'string' ? h : (h.sinif || JSON.stringify(h))}</span>
            </div>
          ))}
        </div>
      )}

      {eksikSiniflar.length > 0 && (
        <div className="semantic-list">
          <p className="semantic-list__title"><AlertCircle size={14} /> Eksik Sınıflar ({eksikSiniflar.length})</p>
          {eksikSiniflar.map((s, i) => (
            <div key={i} className="semantic-item semantic-item--missing">
              <AlertCircle size={13} />
              <span>{typeof s === 'string' ? s : (s.sinif || JSON.stringify(s))}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ── Ana Sayfa ─────────────────────────────────────────────────────────────────

const ResultsPage = ({ data, onNavigate }) => {
  const [showSvg, setShowSvg] = useState(true);
  const [toast, setToast] = useState('');

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 2500);
  };

  if (!data || !data.result) {
    return (
      <div className="page results-page">
        <div className="container">
          <div className="empty-results">
            <BarChart2 size={64} className="empty-results__icon" />
            <h2>Henüz analiz sonucu yok</h2>
            <p>Ana sayfadan bir SRS belgesi yükleyerek analizi başlatın.</p>
            <button className="btn btn-primary" onClick={() => onNavigate('home')}>
              <Home size={18} />
              <span>Ana Sayfaya Dön</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  const { result, srs_metni, document_name } = data;
  const uml = result.uretilen_uml ?? result.plantuml_kodu ?? '';
  const svgContent = result.render?.svg ?? null;
  const siniflar = result.siniflar ?? [];
  const iliskiler = result.iliskiler ?? [];
  const ocl = result.ocl ?? result.dogrulama ?? null;
  const semantik = result.semantik ?? null;
  const sure = result.sure_saniye;

  const hasOclErrors = (ocl?.hatalar ?? []).length > 0;
  const canRepair = hasOclErrors || !(ocl?.gecerli_mi ?? true);

  const handleDownloadPuml = () => {
    downloadPuml(uml, document_name ? `${document_name}.puml` : 'diagram.puml');
    showToast('PlantUML dosyası indirildi.');
  };

  const handleDownloadSvg = () => {
    if (svgContent) {
      downloadSvg(svgContent, document_name ? `${document_name}.svg` : 'diagram.svg');
      showToast('SVG dosyası indirildi.');
    }
  };

  const handleGoRepair = () => {
    onNavigate('repair', {
      plantuml_kodu: uml,
      srs_metni,
      document_name,
    });
  };

  return (
    <div className="page results-page">
      <div className="container">
        {/* Toast */}
        {toast && (
          <div className="toast-notification">
            <CheckCircle size={15} />
            {toast}
          </div>
        )}

        {/* Üst başlık + meta */}
        <div className="results-header">
          <div className="results-header__left">
            <button className="back-btn" onClick={() => onNavigate('home')}>
              <Home size={15} />
              <span>Yeni Analiz</span>
            </button>
            <div className="results-title-block">
              <h2 className="results-title">Analiz Sonuçları</h2>
              <div className="results-meta">
                {document_name && <span className="results-meta__item">📄 {document_name}</span>}
                {sure && <span className="results-meta__item">⏱ {sure}s</span>}
                {result.sla_gecti_mi !== undefined && (
                  <span className={`results-meta__item ${result.sla_gecti_mi ? 'meta-ok' : 'meta-warn'}`}>
                    {result.sla_gecti_mi ? '✓ SLA Geçti' : '⚠ SLA Aşıldı'}
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="results-header__actions">
            {svgContent && (
              <button className="btn-icon" onClick={handleDownloadSvg} title="SVG İndir">
                <Download size={16} />
                <span>SVG</span>
              </button>
            )}
            <button className="btn-icon" onClick={handleDownloadPuml} title="PlantUML İndir">
              <Download size={16} />
              <span>PlantUML</span>
            </button>
            {canRepair && (
              <button className="btn btn-repair" onClick={handleGoRepair}>
                <Wrench size={16} />
                <span>Onarıma Gönder</span>
                <ArrowRight size={16} />
              </button>
            )}
          </div>
        </div>

        {/* Onarım uyarısı */}
        {canRepair && (
          <Alert
            type="error"
            message={`OCL doğrulaması başarısız — ${(ocl?.hatalar ?? []).length} hata tespit edildi. Diyagramı otomatik onarmak için "Onarıma Gönder" düğmesine tıklayın.`}
          />
        )}
        {!canRepair && (
          <Alert
            type="success"
            message="OCL doğrulaması geçti — diyagramda kural ihlali tespit edilmedi."
          />
        )}

        {/* 2 sütunlu ana layout */}
        <div className="results-layout">
          {/* Sol: UML Diyagram */}
          <div className="results-col results-col--diagram">
            <CollapsibleSection title="UML Diyagramı" icon={Eye} badge={svgContent ? 'SVG' : 'Kod'}>
              {/* SVG / PlantUML toggle */}
              {svgContent && (
                <div className="diagram-toggle">
                  <button
                    className={`diagram-toggle__btn ${showSvg ? 'active' : ''}`}
                    onClick={() => setShowSvg(true)}
                  >
                    <Eye size={14} /> Diyagram
                  </button>
                  <button
                    className={`diagram-toggle__btn ${!showSvg ? 'active' : ''}`}
                    onClick={() => setShowSvg(false)}
                  >
                    <Code2 size={14} /> Kod
                  </button>
                </div>
              )}

              {showSvg && svgContent ? (
                <div className="svg-viewer">
                  <div dangerouslySetInnerHTML={{ __html: svgContent }} />
                </div>
              ) : (
                <div className="code-viewer">
                  <div className="code-viewer__toolbar">
                    <span className="code-viewer__lang">PlantUML</span>
                    <CopyButton text={uml} />
                  </div>
                  <pre className="code-viewer__code">{uml}</pre>
                </div>
              )}
            </CollapsibleSection>
          </div>

          {/* Sağ: Metrikler */}
          <div className="results-col results-col--metrics">
            {/* Sınıflar & İlişkiler */}
            <CollapsibleSection title="Sınıflar & İlişkiler" icon={Layers} count={siniflar.length + iliskiler.length}>
              <div className="class-rel-grid">
                <div className="class-list">
                  <p className="class-list__title">
                    <BookOpen size={13} /> Sınıflar ({siniflar.length})
                  </p>
                  {siniflar.length === 0
                    ? <p className="class-list__empty">Sınıf bulunamadı.</p>
                    : siniflar.map((s, i) => (
                      <div key={i} className="class-chip">
                        <Code2 size={12} />
                        {typeof s === 'string' ? s : s.isim ?? JSON.stringify(s)}
                      </div>
                    ))
                  }
                </div>
                <div className="rel-list">
                  <p className="rel-list__title">
                    <ArrowRight size={13} /> İlişkiler ({iliskiler.length})
                  </p>
                  {iliskiler.length === 0
                    ? <p className="rel-list__empty">İlişki bulunamadı.</p>
                    : iliskiler.map((r, i) => (
                      <div key={i} className="rel-chip">
                        {typeof r === 'string' ? r : `${r.kaynak ?? ''} → ${r.hedef ?? ''}`}
                      </div>
                    ))
                  }
                </div>
              </div>
            </CollapsibleSection>

            {/* OCL Doğrulama */}
            <CollapsibleSection
              title="OCL Doğrulama"
              icon={ShieldCheckIcon}
              badge={ocl?.gecerli_mi ? 'Geçti' : 'Başarısız'}
            >
              <OclPanel ocl={ocl} />
            </CollapsibleSection>

            {/* Semantik Değerlendirme */}
            {semantik && (
              <CollapsibleSection
                title="Semantik Sadakat"
                icon={Info}
                badge={semantik?.gecti_mi ? 'Geçti' : 'Düşük'}
              >
                <SemanticPanel semantik={semantik} />
              </CollapsibleSection>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// lucide ShieldCheck için inline wrapper (CollapsibleSection prop olarak alıyor)
const ShieldCheckIcon = (props) => <CheckCircle {...props} />;

export default ResultsPage;
