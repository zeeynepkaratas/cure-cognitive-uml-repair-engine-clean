import { History } from 'lucide-react';
import IterationCard from './IterationCard';

/**
 * Otonom onarımın tüm iterasyonlarını kronolojik timeline olarak gösterir.
 */
const RepairTimeline = ({ iterations }) => {
  if (!iterations || iterations.length === 0) {
    return (
      <div className="repair-timeline__empty">
        <History size={32} />
        <p>Henüz iterasyon başlamadı.</p>
      </div>
    );
  }

  return (
    <div className="repair-timeline">
      <div className="repair-timeline__header">
        <History size={18} />
        <span>İterasyon Zaman Çizelgesi</span>
        <span className="repair-timeline__count">{iterations.length} deneme</span>
      </div>

      <div className="repair-timeline__list">
        {iterations.map((iteration, idx) => (
          <div key={iteration.iteration_no} className="repair-timeline__item">
            {/* Sol dikey çizgi */}
            <div className="repair-timeline__line-wrap">
              <div
                className={`repair-timeline__dot ${
                  iteration.compile_result === 'SUCCESS'
                    ? 'repair-timeline__dot--success'
                    : 'repair-timeline__dot--failed'
                }`}
              />
              {idx < iterations.length - 1 && <div className="repair-timeline__connector" />}
            </div>

            {/* Kart */}
            <div className="repair-timeline__card">
              <IterationCard
                iteration={iteration}
                isLatest={idx === iterations.length - 1}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RepairTimeline;
