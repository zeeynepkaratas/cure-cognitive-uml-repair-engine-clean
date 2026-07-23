/**
 * Hata türü, şiddet seviyesi ve durum bilgisini renkli rozet olarak gösterir.
 * variant: 'type' | 'severity' | 'status' | 'jobStatus'
 */
const LABELS = {
  type: {
    HALLUCINATION: 'Halüsinasyon',
    DESIGN_SMELL: 'Tasarım Kokusu',
    SYNTAX_ERROR: 'Sözdizimi Hatası',
    MISSING_ELEMENT: 'Eksik Eleman',
    INCONSISTENCY: 'Tutarsızlık',
  },
  severity: {
    HIGH: 'Yüksek',
    MEDIUM: 'Orta',
    LOW: 'Düşük',
  },
  status: {
    OPEN: 'Açık',
    ACKNOWLEDGED: 'Görüldü',
    FIXED: 'Düzeltildi',
  },
  jobStatus: {
    COMPLETED: 'Tamamlandı',
    FAILED: 'Başarısız',
    PROCESSING: 'İşleniyor',
  },
};

const CSS_CLASS = {
  type: {
    HALLUCINATION: 'badge--hallucination',
    DESIGN_SMELL: 'badge--design-smell',
    SYNTAX_ERROR: 'badge--syntax-error',
    MISSING_ELEMENT: 'badge--missing',
    INCONSISTENCY: 'badge--inconsistency',
  },
  severity: {
    HIGH: 'badge--high',
    MEDIUM: 'badge--medium',
    LOW: 'badge--low',
  },
  status: {
    OPEN: 'badge--open',
    ACKNOWLEDGED: 'badge--acknowledged',
    FIXED: 'badge--fixed',
  },
  jobStatus: {
    COMPLETED: 'badge--fixed',
    FAILED: 'badge--high',
    PROCESSING: 'badge--acknowledged',
  },
};

const StatusBadge = ({ variant = 'type', value }) => {
  if (!value) return null;

  const label = LABELS[variant]?.[value] ?? value;
  const cssClass = CSS_CLASS[variant]?.[value] ?? '';

  return (
    <span className={`badge ${cssClass}`} title={label}>
      {label}
    </span>
  );
};

export default StatusBadge;
