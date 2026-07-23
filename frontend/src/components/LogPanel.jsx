import { useState } from 'react';
import {
  Clock,
  FileText,
  CheckCircle,
  XCircle,
  AlertTriangle,
  ChevronRight,
} from 'lucide-react';
import StatusBadge from './StatusBadge';
import { formatTimestamp } from '../utils';

const JOB_STATUS_ICON = {
  COMPLETED: CheckCircle,
  FAILED: XCircle,
  PROCESSING: Clock,
};

const LogRow = ({ log, onSelect, isActive }) => {
  const StatusIcon = JOB_STATUS_ICON[log.status] ?? Clock;

  return (
    <button
      className={`log-row ${isActive ? 'log-row--active' : ''} log-row--${log.status.toLowerCase()}`}
      onClick={() => onSelect(log)}
      aria-pressed={isActive}
    >
      <div className="log-row__icon">
        <StatusIcon size={18} />
      </div>

      <div className="log-row__info">
        <span className="log-row__doc">
          <FileText size={13} />
          {log.document}
        </span>
        <span className="log-row__time">
          <Clock size={12} />
          {formatTimestamp(log.timestamp)}
        </span>
      </div>

      <div className="log-row__stats">
        <StatusBadge variant="jobStatus" value={log.status} />
        {log.status !== 'FAILED' && (
          <span className="log-row__error-count">
            {log.error_count > 0 && (
              <>
                <AlertTriangle size={12} />
                {log.error_count} hata
                {log.high_count > 0 && (
                  <span className="log-row__high-count">
                    ({log.high_count} yüksek)
                  </span>
                )}
              </>
            )}
            {log.error_count === 0 && (
              <span className="log-row__clean">Temiz</span>
            )}
          </span>
        )}
      </div>

      <ChevronRight size={16} className="log-row__arrow" />
    </button>
  );
};

const LogPanel = ({ logs = [], onSelectJob }) => {
  const [selectedId, setSelectedId] = useState(logs[0]?.id ?? null);

  const handleSelect = (log) => {
    setSelectedId(log.id);
    onSelectJob?.(log);
  };

  return (
    <div className="log-panel">
      <div className="log-panel__header">
        <h3 className="log-panel__title">
          <Clock size={18} />
          Analiz Geçmişi
        </h3>
        <span className="log-panel__subtitle">{logs.length} kayıt</span>
      </div>

      {logs.length === 0 ? (
        <div className="log-panel__empty">
          <Clock size={40} />
          <p>Henüz analiz kaydı yok.</p>
        </div>
      ) : (
        <div className="log-panel__list">
          {logs.map((log) => (
            <LogRow
              key={log.id}
              log={log}
              onSelect={handleSelect}
              isActive={log.id === selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default LogPanel;
