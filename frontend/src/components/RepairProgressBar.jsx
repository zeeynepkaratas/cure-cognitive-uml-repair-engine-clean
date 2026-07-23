import { CheckCircle, Loader, Circle } from 'lucide-react';

const REPAIR_PHASES_ORDERED = [
  { key: 'ANALIZ',        label: 'Analiz',       description: 'OCL kuralları ile diyagram taranıyor' },
  { key: 'ONARIM',        label: 'Onarım',        description: 'Healer ajanı düzeltmeleri uyguluyor' },
  { key: 'DERLEME_TESTI', label: 'Derleme Testi', description: 'Compile testi çalıştırılıyor' },
  { key: 'TAMAMLANDI',    label: 'Tamamlandı',    description: 'İterasyon sonuçlandı' },
];

const REPAIR_STATUS = {
  SUCCESS: 'SUCCESS',
  FAILED: 'FAILED',
  IN_PROGRESS: 'IN_PROGRESS',
};

/**
 * Otonom onarım sürecinin iterasyon bazlı ilerleme çubuğu.
 * Dört faz gösterir: Analiz → Onarım → Derleme Testi → Tamamlandı
 */
const RepairProgressBar = ({ currentPhase, iterationNo, maxIterations, overallStatus }) => {
  const currentPhaseIndex = REPAIR_PHASES_ORDERED.findIndex((p) => p.key === currentPhase);
  const iterationProgress = Math.min((iterationNo / maxIterations) * 100, 100);
  const isFailed = overallStatus === REPAIR_STATUS.FAILED;

  return (
    <div className="repair-progress">
      <div className="repair-progress__header">
        <div className="repair-progress__title">
          {isFailed ? (
            <span className="repair-progress__label repair-progress__label--failed">
              Onarım Tamamlanamadı
            </span>
          ) : overallStatus === REPAIR_STATUS.SUCCESS ? (
            <span className="repair-progress__label repair-progress__label--success">
              Onarım Başarıyla Tamamlandı
            </span>
          ) : (
            <span className="repair-progress__label repair-progress__label--active">
              Otonom Onarım Devam Ediyor
            </span>
          )}
        </div>
        <div className="repair-progress__iteration-badge">
          Deneme {iterationNo} / {maxIterations}
        </div>
      </div>

      {/* Yüzde bazlı bar */}
      <div className="repair-progress__bar-wrap">
        <div
          className={`repair-progress__bar ${isFailed ? 'repair-progress__bar--failed' : ''}`}
          style={{ width: `${iterationProgress}%` }}
          role="progressbar"
          aria-valuenow={iterationProgress}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>

      {/* Adım etiketleri */}
      <div className="repair-progress__steps">
        {REPAIR_PHASES_ORDERED.map((phase, idx) => {
          const isDone = idx < currentPhaseIndex || overallStatus !== REPAIR_STATUS.IN_PROGRESS;
          const isActive = idx === currentPhaseIndex && overallStatus === REPAIR_STATUS.IN_PROGRESS;
          const isPending = idx > currentPhaseIndex && overallStatus === REPAIR_STATUS.IN_PROGRESS;

          return (
            <div
              key={phase.key}
              className={`repair-step ${isDone ? 'repair-step--done' : ''} ${isActive ? 'repair-step--active' : ''} ${isPending ? 'repair-step--pending' : ''}`}
            >
              <div className="repair-step__icon">
                {isDone ? (
                  <CheckCircle size={18} />
                ) : isActive ? (
                  <Loader size={18} className="spin-icon" />
                ) : (
                  <Circle size={18} />
                )}
              </div>
              <div className="repair-step__info">
                <span className="repair-step__label">{phase.label}</span>
                <span className="repair-step__desc">{phase.description}</span>
              </div>
              {idx < REPAIR_PHASES_ORDERED.length - 1 && (
                <div className={`repair-step__connector ${isDone ? 'repair-step__connector--done' : ''}`} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RepairProgressBar;
