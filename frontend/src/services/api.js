import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Axios error'dan okunabilir Türkçe mesaj çıkarır.
 */
function getErrorMessage(error, fallback) {
  const data = error.response?.data;
  if (!data) return fallback;
  if (typeof data.message === 'string') return data.message;
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail) && data.detail[0]?.msg) {
    return data.detail.map((d) => d.msg).join(' ');
  }
  return fallback;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000, // AI işlemleri uzun sürebilir
});

// ── Sağlık Kontrolü ──────────────────────────────────────────────────────────

/** Backend'in ayakta olup olmadığını kontrol eder. */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return { online: true, data: response.data };
  } catch {
    return { online: false, data: null };
  }
};

// ── Çekirdek Analiz ──────────────────────────────────────────────────────────

/**
 * SRS metnini tam pipeline'dan geçirir:
 * SRS → PlantUML üret → OCL doğrula → Semantik değerlendir
 * En kapsamlı endpoint — ana analiz akışı için kullan.
 */
export const analyzeDocument = async (metin, dil = 'en') => {
  try {
    const response = await api.post('/api/analyze', { metin, dil });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Tam analiz yapılırken bir hata oluştu');
  }
};

/**
 * Sadece SRS → PlantUML üretimi + OCL doğrulama + render.
 * Semantik değerlendirme dahil değil.
 */
export const parseDocument = async (metin, dil = 'en') => {
  try {
    const response = await api.post('/api/parse', { metin, dil });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Metin işlenirken bir hata oluştu');
  }
};

// ── UML İşlemleri ─────────────────────────────────────────────────────────────

/**
 * PlantUML kodunu OCL kurallarıyla doğrular.
 */
export const validateUML = async (plantuml_kodu) => {
  try {
    const response = await api.post('/api/validate', { plantuml_kodu });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'OCL doğrulama sırasında bir hata oluştu');
  }
};

/**
 * PlantUML kodunu SVG/PNG olarak render eder.
 */
export const renderUML = async (plantuml_kodu) => {
  try {
    const response = await api.post('/api/render', { plantuml_kodu });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Render sırasında bir hata oluştu');
  }
};

/**
 * SRS + PlantUML kodu için semantik sadakat skoru hesaplar.
 */
export const evaluateUML = async (srs_metni, plantuml_kodu) => {
  try {
    const response = await api.post('/api/evaluate', { srs_metni, plantuml_kodu });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Semantik değerlendirme sırasında bir hata oluştu');
  }
};

// ── Otonom Onarım ─────────────────────────────────────────────────────────────

/**
 * Gerçek AI ajanıyla otonom UML onarımı.
 * max_iterations: 1-5 arası (backend limiti).
 */
export const autonomousRepair = async (plantuml_kodu, srs_metni = null, max_iterations = 3) => {
  try {
    const response = await api.post('/api/autonomous-repair', {
      plantuml_kodu,
      srs_metni,
      max_iterations,
    });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Otonom onarım sırasında bir hata oluştu');
  }
};

/**
 * Tek iterasyon compile + opsiyonel semantik test.
 */
export const runIteration = async (plantuml_kodu, iterasyon_no = 1, srs_metni = null) => {
  try {
    const response = await api.post('/api/iterate', {
      plantuml_kodu,
      iterasyon_no,
      srs_metni,
    });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'İterasyon testi sırasında bir hata oluştu');
  }
};

// ── Hata Günlüğü ─────────────────────────────────────────────────────────────

/**
 * Kayıtlı hata loglarını getirir.
 * kategori: 'SYNTAX' | 'OCL' | 'SEMANTIC' | 'HALLUCINATION' | null (tümü)
 */
export const getErrorLogs = async (kategori = null, son_n = 50) => {
  try {
    const params = { son_n };
    if (kategori) params.kategori = kategori;
    const response = await api.get('/api/error-log', { params });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Hata günlüğü yüklenirken bir sorun oluştu');
  }
};

/**
 * Tüm hata loglarını temizler.
 */
export const clearErrorLogs = async () => {
  try {
    const response = await api.delete('/api/error-log');
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Loglar temizlenirken bir hata oluştu');
  }
};

// ── Performans ─────────────────────────────────────────────────────────────────

/**
 * Performans metriklerini (P50/P95/P99, SLA) getirir.
 */
export const getPerformance = async (endpoint = null) => {
  try {
    const params = endpoint ? { endpoint } : {};
    const response = await api.get('/api/performance', { params });
    return response.data;
  } catch (error) {
    throw getErrorMessage(error, 'Performans verileri yüklenirken bir hata oluştu');
  }
};

export default api;