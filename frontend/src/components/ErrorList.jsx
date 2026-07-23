import { useState } from 'react';
import {
  AlertTriangle,
  AlertCircle,
  Info,
  ChevronDown,
  ChevronUp,
  Lightbulb,
  Code2,
  GitBranch,
} from 'lucide-react';
import StatusBadge from './StatusBadge';
import { formatTimestamp } from '../utils';

const TYPE_ICONS = {
  HALLUCINATION: AlertTriangle,
  DESIGN_SMELL: GitBranch,
  SYNTAX_ERROR: Code2,
  MISSING_ELEMENT: AlertCircle,
  INCONSISTENCY: Info,
};

const FILTER_OPTIONS = [
  { value: 'ALL', label: 'Tümü' },
  { value: 'HALLUCINATION', label: 'Halüsinasyon' },
  { value: 'DESIGN_SMELL', label: 'Tasarım Kokusu' },
  { value: 'SYNTAX_ERROR', label: 'Sözdizimi Hatası' },
  { value: 'MISSING_ELEMENT', label: 'Eksik Eleman' },
  { value: 'INCONSISTENCY', label: 'Tutarsızlık' },
];

const SEVERITY_ORDER = { HIGH: 0, MEDIUM: 1, LOW: 2 };

const ErrorItem = ({ error }) => {
  const [expanded, setExpanded] = useState(false);
  const [tooltipVisible, setTooltipVisible] = useState(false);

  const Icon = TYPE_ICONS[error.type] ?? AlertCircle;
  const isHigh = error.severity === 'HIGH';

  return (
    <div
      className={`error-item ${isHigh ? 'error-item--high' : ''} error-item--${error.severity.toLowerCase()}`}
    >
      <div
        className="error-item__header"
        onClick={() => setExpanded((v) => !v)}
        onMouseEnter={() => setTooltipVisible(true)}
        onMouseLeave={() => setTooltipVisible(false)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <div className="error-item__icon-wrap">
          <Icon size={18} />
        </div>

        <div className="error-item__meta">
          <span className="error-item__element">{error.element}</span>
          <span className="error-item__element-type">{error.element_type}</span>
          {error.line && (
            <span className="error-item__line">Satır {error.line}</span>
          )}
        </div>

        <div className="error-item__badges">
          <StatusBadge variant="type" value={error.type} />
          <StatusBadge variant="severity" value={error.severity} />
          <StatusBadge variant="status" value={error.status} />
        </div>

        <button className="error-item__toggle" aria-label="Detayı göster/gizle">
          {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>

        {tooltipVisible && !expanded && (
          <div className="error-tooltip" role="tooltip">
            <p className="error-tooltip__desc">{error.description}</p>
            {error.suggestion && (
              <p className="error-tooltip__suggestion">
                <Lightbulb size={12} /> {error.suggestion}
              </p>
            )}
          </div>
        )}
      </div>

      {expanded && (
        <div className="error-item__body">
          <p className="error-item__description">{error.description}</p>
          {error.suggestion && (
            <div className="error-item__suggestion">
              <Lightbulb size={14} />
              <span>{error.suggestion}</span>
            </div>
          )}
          <p className="error-item__timestamp">
            Tespit: {formatTimestamp(error.detected_at)}
          </p>
        </div>
      )}
    </div>
  );
};

const ErrorList = ({ errors = [] }) => {
  const [filterType, setFilterType] = useState('ALL');
  const [filterSeverity, setFilterSeverity] = useState('ALL');

  const filtered = errors
    .filter((e) => filterType === 'ALL' || e.type === filterType)
    .filter((e) => filterSeverity === 'ALL' || e.severity === filterSeverity)
    .sort((a, b) => SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity]);

  return (
    <div className="error-list">
      <div className="error-list__toolbar">
        <div className="error-list__filters">
          <select
            className="filter-select"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            aria-label="Hata türüne göre filtrele"
          >
            {FILTER_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>

          <select
            className="filter-select"
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            aria-label="Şiddete göre filtrele"
          >
            <option value="ALL">Tüm Şiddetler</option>
            <option value="HIGH">Yüksek</option>
            <option value="MEDIUM">Orta</option>
            <option value="LOW">Düşük</option>
          </select>
        </div>

        <span className="error-list__count">
          {filtered.length} / {errors.length} hata gösteriliyor
        </span>
      </div>

      {filtered.length === 0 ? (
        <div className="error-list__empty">
          <AlertCircle size={40} />
          <p>Bu filtreyle eşleşen hata bulunamadı.</p>
        </div>
      ) : (
        <div className="error-list__items">
          {filtered.map((error) => (
            <ErrorItem key={error.id} error={error} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ErrorList;
