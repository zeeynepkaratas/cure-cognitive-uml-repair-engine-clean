import { useState, useEffect, useCallback } from 'react';
import {
  AlertTriangle, AlertCircle, CheckCircle, Clock,
  RefreshCw, Trash2, Filter, BookOpen,
} from 'lucide-react';
import { getErrorLogs, clearErrorLogs } from '../services/api';
import { formatTimestamp } from '../utils';
import Alert from '../components/Alert';

// ── Filtre seçenekleri ───────────────────────────────────────────────────────
const KATEGORI_OPTIONS = [
  { value: '', label: 'Tüm Kategoriler' },
  { value: 'SYNTAX', label: 'Sözdizimi (SYNTAX)' },
  { value: 'OCL', label: 'OCL' },
  { value: 'SEMANTIC', label: 'Semantik' },
  { value: 'HALLUCINATION', label: 'Halüsinasyon' },
  { value: 'AI_HEALER_FAILED', label: 'AI Healer Başarısız' },
];

const KAT_ICON = {
  SYNTAX: AlertCircle,
  OCL: BookOpen,
  SEMANTIC: AlertTriangle,
  HALLUCINATION: AlertTriangle,
  AI_HEALER_FAILED: AlertCircle,
};

const KAT_COLOR = {
  SYNTAX: 'badge--syntax-error',
  OCL: 'badge--missing',
  SEMANTIC: 'badge--design-smell',
  HALLUCINATION: 'badge--hallucination',
  AI_HEALER_FAILED: 'badge--high',
};

// ── Tek log satırı ───────────────────────────────────────────────────────────
const LogEntry = ({ log }) => {
  const [expanded, setExpanded] = useState(false);
  const Icon = KAT_ICON[log.kategori] ?? AlertCircle;
  const catClass = KAT_COLOR[log.kategori] ?? '';

  return (
    <div className={`log-entry ${expanded ? 'log-entry--open' : ''}`}>
      <button
        className="log-entry__header"
        onClick={() => setExpanded(v => !v)}
        aria-expanded={expanded}
      >
        <div className="log-entry__icon">
          <Icon size={16} />
        </div>
        <div className="log-entry__info">
          <span className="log-entry__msg">{log.mesaj}</span>
          <span className="log-entry__time">
            <Clock size={11} />
            {formatTimestamp(log.zaman)}
          </span>
        </div>
        <div className="log-entry__right">
          <span className={`badge ${catClass}`}>{log.kategori}</span>
          {log.iterasyon_no != null && (
            <span className="log-entry__iter">#{log.iterasyon_no}. iter</span>
          )}
          <span className="log-entry__id">#{log.log_id}</span>
        </div>
      </button>

      {expanded && (
        <div className="log-entry__body">
          {log.skor != null && (
            <p className="log-entry__skor">
              Skor: <strong>{typeof log.skor === 'number' ? `${(log.skor * 100).toFixed(0)}%` : log.skor}</strong>
            </p>
          )}
          {log.plantuml_kodu && (
            <div className="code-viewer" style={{ marginTop: 12 }}>
              <div className="code-viewer__toolbar">
                <span className="code-viewer__lang">PlantUML</span>
              </div>
              <pre className="code-viewer__code" style={{ maxHeight: 200, overflowY: 'auto' }}>
                {log.plantuml_kodu}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ── Ana Sayfa ─────────────────────────────────────────────────────────────────
const ErrorLogPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [fetchError, setFetchError] = useState('');
  const [toast, setToast] = useState('');
  const [kategori, setKategori] = useState('');
  const [sonN, setSonN] = useState(50);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 2500);
  };

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setFetchError('');
    try {
      const data = await getErrorLogs(kategori || null, sonN);
      setLogs(data.loglar ?? []);
    } catch (err) {
      setFetchError(typeof err === 'string' ? err : 'Hata günlüğü yüklenemedi.');
    } finally {
      setLoading(false);
    }
  }, [kategori, sonN]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  const handleClear = async () => {
    if (!window.confirm('Tüm hata logları silinecek. Emin misiniz?')) return;
    setClearing(true);
    try {
      await clearErrorLogs();
      setLogs([]);
      showToast('Tüm loglar temizlendi.');
    } catch (err) {
      setFetchError(typeof err === 'string' ? err : 'Loglar temizlenemedi.');
    } finally {
      setClearing(false);
    }
  };

  // Kategori dağılımı (özet)
  const summary = KATEGORI_OPTIONS.slice(1).reduce((acc, opt) => {
    acc[opt.value] = logs.filter(l => l.kategori === opt.value).length;
    return acc;
  }, {});

  return (
    <div className="page error-log-page">
      <div className="container">
        {toast && (
          <div className="toast-notification">
            <CheckCircle size={15} />
            {toast}
          </div>
        )}

        {/* Başlık */}
        <div className="content-card">
          <div className="card-header">
            <h2>Hata Günlüğü</h2>
            <p>
              Backend'in kaydettiği tüm analiz ve onarım hataları. Veriler
              backend çalıştığı sürece saklanır; yeniden başlatmada sıfırlanır.
            </p>
          </div>

          {fetchError && (
            <Alert type="error" message={fetchError} onClose={() => setFetchError('')} />
          )}

          {/* Özet kartları */}
          <div className="summary-grid">
            <div className="summary-card summary-card--neutral">
              <div className="summary-card__icon"><AlertCircle size={20} /></div>
              <div className="summary-card__body">
                <span className="summary-card__value">{logs.length}</span>
                <span className="summary-card__label">Toplam Log</span>
              </div>
            </div>
            <div className="summary-card summary-card--high">
              <div className="summary-card__icon"><AlertTriangle size={20} /></div>
              <div className="summary-card__body">
                <span className="summary-card__value">{(summary.SYNTAX ?? 0) + (summary.OCL ?? 0)}</span>
                <span className="summary-card__label">Syntax / OCL</span>
              </div>
            </div>
            <div className="summary-card summary-card--medium">
              <div className="summary-card__icon"><AlertTriangle size={20} /></div>
              <div className="summary-card__body">
                <span className="summary-card__value">{(summary.HALLUCINATION ?? 0) + (summary.SEMANTIC ?? 0)}</span>
                <span className="summary-card__label">Halüsinasyon / Semantik</span>
              </div>
            </div>
            <div className="summary-card summary-card--fixed">
              <div className="summary-card__icon"><CheckCircle size={20} /></div>
              <div className="summary-card__body">
                <span className="summary-card__value">{summary.AI_HEALER_FAILED ?? 0}</span>
                <span className="summary-card__label">Healer Başarısız</span>
              </div>
            </div>
          </div>

          {/* Araç çubuğu */}
          <div className="log-toolbar">
            <div className="log-toolbar__filters">
              <Filter size={15} />
              <select
                className="filter-select"
                value={kategori}
                onChange={e => setKategori(e.target.value)}
                aria-label="Kategoriye göre filtrele"
              >
                {KATEGORI_OPTIONS.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
              <select
                className="filter-select"
                value={sonN}
                onChange={e => setSonN(Number(e.target.value))}
                aria-label="Gösterilecek kayıt sayısı"
              >
                <option value={20}>Son 20</option>
                <option value={50}>Son 50</option>
                <option value={100}>Son 100</option>
              </select>
            </div>
            <div className="log-toolbar__actions">
              <button
                className="btn-icon"
                onClick={fetchLogs}
                disabled={loading}
                title="Yenile"
              >
                <RefreshCw size={15} className={loading ? 'spin-icon' : ''} />
                <span>Yenile</span>
              </button>
              <button
                className="btn-icon btn-icon--danger"
                onClick={handleClear}
                disabled={clearing || logs.length === 0}
                title="Logları Temizle"
              >
                <Trash2 size={15} />
                <span>Temizle</span>
              </button>
            </div>
          </div>

          {/* Log listesi */}
          {loading ? (
            <div className="log-loading">
              <div className="spinner" />
              <p>Loglar yükleniyor…</p>
            </div>
          ) : logs.length === 0 ? (
            <div className="log-empty">
              <CheckCircle size={48} className="icon-success" />
              <h3>Hata Logu Bulunamadı</h3>
              <p>
                {kategori
                  ? `"${kategori}" kategorisinde kayıt yok.`
                  : 'Henüz sistem tarafından kaydedilmiş bir hata yok. Bu iyiye işaret!'}
              </p>
            </div>
          ) : (
            <div className="log-list">
              <div className="log-list__count">
                {logs.length} kayıt gösteriliyor
              </div>
              {logs.map(log => (
                <LogEntry key={log.log_id} log={log} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorLogPage;
