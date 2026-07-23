import { AlertCircle, CheckCircle, Info } from 'lucide-react';

const Alert = ({ type = 'info', message, onClose }) => {
  const icons = {
    error: <AlertCircle size={20} />,
    success: <CheckCircle size={20} />,
    info: <Info size={20} />
  };

  return (
    <div className={`alert alert-${type}`}>
      <div className="alert-icon">{icons[type]}</div>
      <p className="alert-message">{message}</p>
      {onClose && (
        <button onClick={onClose} className="alert-close" aria-label="Kapat">
          ×
        </button>
      )}
    </div>
  );
};

export default Alert;
