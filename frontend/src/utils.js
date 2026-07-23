/**
 * CURE — Ortak yardımcı fonksiyonlar
 * mockData.js'den taşınan ve yeni eklenen utility'ler buradadır.
 */

/** ISO zaman dizgisini Türkçe yerel formata çevirir. */
export const formatTimestamp = (isoString) => {
  if (!isoString) return '—';
  const date = new Date(isoString);
  return date.toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/** Milisaniyeyi okunabilir biçime çevirir ("1.4s" gibi). */
export const formatDuration = (ms) => {
  if (ms == null) return '—';
  return `${(ms / 1000).toFixed(1)}s`;
};

/** Skoru yüzdeye çevirir, 0-100 aralığında döner. */
export const scoreToPercent = (score, max = 1) => {
  if (score == null || max === 0) return 0;
  return Math.round((score / max) * 100);
};

/** Renk kodu: skor yüzdesine göre yeşil / sarı / kırmızı */
export const scoreColor = (percent) => {
  if (percent >= 80) return 'var(--success)';
  if (percent >= 50) return 'var(--warning)';
  return 'var(--error)';
};

/** Metni panoya kopyalar. Geri promise döner. */
export const copyToClipboard = (text) => {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  }
  // Fallback
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
  return Promise.resolve();
};

/** PlantUML kodunu .puml dosyası olarak indirir. */
export const downloadPuml = (code, filename = 'diagram.puml') => {
  const blob = new Blob([code], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

/** SVG stringini .svg dosyası olarak indirir. */
export const downloadSvg = (svgString, filename = 'diagram.svg') => {
  const blob = new Blob([svgString], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

/** localStorage'a analiz geçmişi kaydeder (max 20 kayıt). */
export const saveToHistory = (entry) => {
  try {
    const key = 'cure_analysis_history';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    const updated = [entry, ...existing].slice(0, 20);
    localStorage.setItem(key, JSON.stringify(updated));
  } catch (_) {
    // localStorage erişim hatalarını yut
  }
};

/** localStorage'dan analiz geçmişini okur. */
export const loadHistory = () => {
  try {
    return JSON.parse(localStorage.getItem('cure_analysis_history') || '[]');
  } catch (_) {
    return [];
  }
};

/** Geçmişi temizler. */
export const clearHistory = () => {
  try {
    localStorage.removeItem('cure_analysis_history');
  } catch (_) {}
};
