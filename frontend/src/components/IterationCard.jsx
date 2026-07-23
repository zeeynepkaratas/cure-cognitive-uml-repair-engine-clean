import { useState } from 'react';
import {
  CheckCircle,
  XCircle,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Wrench,
  Code,
  BookOpen,
} from 'lucide-react';
import { formatTimestamp } from '../utils';
import StatusBadge from './StatusBadge';

const ERROR_TYPES = {
  HALLUCINATION: 'HALLUCINATION',
  DESIGN_SMELL: 'DESIGN_SMELL',
  SYNTAX_ERROR: 'SYNTAX_ERROR',
  MISSING_ELEMENT: 'MISSING_ELEMENT',
  INCONSISTENCY: 'INCONSISTENCY',
};

const REPAIR_STATUS = {
  SUCCESS: 'SUCCESS',
  FAILED: 'FAILED',
  IN_PROGRESS: 'IN_PROGRESS',
};

const ERROR_TYPE_LABEL = {
  [ERROR_TYPES.HALLUCINATION]: 'Halüsinasyon',
  [ERROR_TYPES.DESIGN_SMELL]: 'Tasarım Kokusu',
  [ERROR_TYPES.SYNTAX_ERROR]: 'Sözdizimi Hatası',
  [ERROR_TYPES.MISSING_ELEMENT]: 'Eksik Eleman',
  [ERROR_TYPES.INCONSISTENCY]: 'Tutarsızlık',
};

/**
 * Tek bir iterasyon deneme kartı.
 * Hata tipi, düzeltme özeti, OCL kuralı ve compile sonucunu gösterir.
 */
const IterationCard = ({ iteration, isLatest }) => {
  const [expanded, setExpanded] = useState(isLatest);
  const isSuccess = iteration.compile_result === REPAIR_STATUS.SUCCESS;
  const isFailed = iteration.compile_result === REPAIR_STATUS.FAILED;

  return (
    <div
      className={`iteration-card ${isSuccess ? 'iteration-card--success' : 'iteration-card--failed'} ${isLatest ? 'iteration-card--latest' : ''}`}
    >
      {/* Kart başlığı */}
      <button
        className="iteration-card__header"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <div className="iteration-card__number">
          {isSuccess ? (
            <CheckCircle size={20} className="icon-success" />
          ) : (
            <XCircle size={20} className="icon-failed" />
          )}
          <span>Deneme {iteration.iteration_no}</span>
          {isLatest && <span className="iteration-card__latest-badge">Son</span>}
        </div>

        <div className="iteration-card__meta">
          <span className="iteration-card__compile">
            {isSuccess ? (
              <span className="compile-ok">Derleme: Başarılı</span>
            ) : (
              <span className="compile-fail">Derleme: Başarısız</span>
            )}
          </span>
          <span className="iteration-card__duration">
            {(iteration.duration_ms / 1000).toFixed(1)}s
          </span>
          <span className="iteration-card__time">
            {formatTimestamp(iteration.started_at)}
          </span>
        </div>

        <div className="iteration-card__toggle">
          {expanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </div>
      </button>

      {/* Hata önizlemesi (her zaman görünür) */}
      <div className="iteration-card__errors-preview">
        {iteration.errors_found.map((err) => (
          <span key={err.id} className="iteration-card__err-chip">
            <AlertTriangle size={11} />
            {err.element}
            <span className="chip-type">{ERROR_TYPE_LABEL[err.type] ?? err.type}</span>
          </span>
        ))}
      </div>

      {/* Genişletilmiş içerik */}
      {expanded && (
        <div className="iteration-card__body">
          {/* OCL Kuralı */}
          <div className="iteration-section">
            <div className="iteration-section__title">
              <BookOpen size={14} />
              Uygulanan OCL Kuralı
            </div>
            <code className="iteration-ocl">{iteration.ocl_rule_used}</code>
          </div>

          {/* Düzeltme Özeti */}
          <div className="iteration-section">
            <div className="iteration-section__title">
              <Wrench size={14} />
              Düzeltme Özeti
            </div>
            <p className="iteration-fix-summary">{iteration.fix_summary}</p>
          </div>

          {/* Diff */}
          <div className="iteration-section">
            <div className="iteration-section__title">
              <Code size={14} />
              Uygulanan Değişiklik
            </div>
            <pre className="iteration-diff">{iteration.fix_diff}</pre>
          </div>

          {/* Compile Sonucu */}
          {isFailed && iteration.compile_error && (
            <div className="iteration-compile-error">
              <XCircle size={14} />
              <span>{iteration.compile_error}</span>
            </div>
          )}

          {isSuccess && (
            <div className="iteration-compile-success">
              <CheckCircle size={14} />
              <span>Derleme testi geçti — bu iterasyon onaylandı.</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default IterationCard;
