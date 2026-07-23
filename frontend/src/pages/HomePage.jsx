import { useState, useCallback } from 'react';
import FileUpload from '../components/FileUpload';
import Alert from '../components/Alert';
import { analyzeDocument } from '../services/api';
import { saveToHistory } from '../utils';
import { ArrowRight, Cpu, ShieldCheck, Zap, FileSearch } from 'lucide-react';

const SRS_ACCEPT = {
  'text/plain': ['.txt'],
  'application/pdf': ['.pdf'],
};

const UML_ACCEPT = {
  'application/xml': ['.xmi', '.uml'],
  'text/xml': ['.xmi', '.uml'],
  'text/plain': ['.puml', '.plantuml'],
};

const FEATURES = [
  {
    icon: FileSearch,
    title: 'SRS Analizi',
    desc: 'Gereksinim belgenizi NLP ile işler, sınıf ve ilişkileri otomatik çıkarır.',
  },
  {
    icon: ShieldCheck,
    title: 'OCL Doğrulama',
    desc: 'Object Constraint Language kurallarıyla diyagramınızı katı biçimde doğrular.',
  },
  {
    icon: Cpu,
    title: 'Otonom Onarım',
    desc: 'Çoklu-etmen AI sistemi halüsinasyon ve tutarsızlıkları tespit edip düzeltir.',
  },
  {
    icon: Zap,
    title: 'Anında Sonuç',
    desc: 'İşlem süresi genellikle 15 saniyenin altındadır; SLA garantili.',
  },
];

const HomePage = ({ onNavigate }) => {
  const [srsFile, setSrsFile] = useState(null);
  const [umlFile, setUmlFile] = useState(null);
  const [uploadResetKey, setUploadResetKey] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [srsUploadError, setSrsUploadError] = useState('');
  const [umlUploadError, setUmlUploadError] = useState('');

  const handleSrsSelect = useCallback((file, err = '') => {
    setSrsFile(file);
    setSrsUploadError(err);
    setError('');
  }, []);

  const handleUmlSelect = useCallback((file, err = '') => {
    setUmlFile(file);
    setUmlUploadError(err);
    setError('');
  }, []);

  const handleSubmit = async () => {
    if (!srsFile) {
      setError('Lütfen SRS belgesi (.txt veya .pdf) yükleyin');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const srsMetni = await srsFile.text();
      let umlMetni = null;
      if (umlFile) {
        umlMetni = await umlFile.text();
      }

      // Tam analiz pipeline'ı çağır
      const result = await analyzeDocument(srsMetni);

      // Geçmişe kaydet (localStorage)
      saveToHistory({
        id: `job_${Date.now()}`,
        timestamp: new Date().toISOString(),
        document: srsFile.name,
        srs_metni: srsMetni,
        result,
      });

      // Dosyaları sıfırla
      setSrsFile(null);
      setUmlFile(null);
      setUploadResetKey((k) => k + 1);

      // Sonuçlar sayfasına geç ve analiz verisini aktar
      onNavigate('results', {
        result,
        srs_metni: srsMetni,
        uml_metni: umlMetni,
        document_name: srsFile.name,
      });
    } catch (err) {
      setError(typeof err === 'string' ? err : 'Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page home-page">
      <div className="container">
        {/* Hero */}
        <div className="home-hero">
          <div className="home-hero__badge">
            <Cpu size={14} />
            <span>AI Destekli UML Onarım</span>
          </div>
          <h2 className="home-hero__title">
            SRS'den Doğrulanmış<br />
            <span className="gradient-text">UML'ye</span>
          </h2>
          <p className="home-hero__sub">
            Yazılım gereksinim belgenizi yükleyin — sistem OCL kuralları ve çoklu-etmen AI
            ile UML diyagramınızı otomatik üretir, doğrular ve onarır.
          </p>
        </div>

        {/* Upload kartı */}
        <div className="content-card upload-card">
          <div className="upload-stack">
            <FileUpload
              key={`srs-${uploadResetKey}`}
              onFileSelect={handleSrsSelect}
              error={srsUploadError}
              loading={loading}
              accept={SRS_ACCEPT}
              title="SRS Belgesi"
              emptyDescription="SRS dosyanızı (.txt veya .pdf) sürükleyip bırakın veya seçmek için tıklayın"
              fileHint="Zorunlu · En fazla 10 MB"
              invalidTypeMessage="SRS için yalnızca .txt ve .pdf kabul edilir"
            />
            <FileUpload
              key={`uml-${uploadResetKey}`}
              onFileSelect={handleUmlSelect}
              error={umlUploadError}
              loading={loading}
              accept={UML_ACCEPT}
              title="Mevcut UML (isteğe bağlı)"
              emptyDescription="XMI (.xmi) veya PlantUML (.puml, .plantuml) dosyanızı ekleyin"
              fileHint="İsteğe bağlı · En fazla 10 MB"
              variant="compact"
              invalidTypeMessage="UML için .xmi, .uml, .puml veya .plantuml kullanın"
            />
          </div>

          {error && (
            <Alert type="error" message={error} onClose={() => setError('')} />
          )}

          {loading ? (
            <div className="analyze-loading">
              <div className="analyze-loading__bar">
                <div className="analyze-loading__fill" />
              </div>
              <div className="analyze-loading__steps">
                <span className="step-chip step-chip--active">SRS Ayrıştırılıyor</span>
                <span className="step-chip">UML Üretiliyor</span>
                <span className="step-chip">OCL Doğrulanıyor</span>
                <span className="step-chip">Semantik Analiz</span>
              </div>
              <p className="analyze-loading__msg">
                Bu işlem 5-15 saniye sürebilir, lütfen bekleyin…
              </p>
            </div>
          ) : (
            <button
              onClick={handleSubmit}
              className="btn btn-primary btn-analyze"
              disabled={!srsFile}
              id="analyze-btn"
            >
              <span>Analizi Başlat</span>
              <ArrowRight size={20} />
            </button>
          )}
        </div>

        {/* Özellik kartları */}
        <div className="features-section">
          <h3 className="features-title">Sistem Nasıl Çalışır?</h3>
          <div className="features-grid">
            {FEATURES.map((f, i) => {
              const Icon = f.icon;
              return (
                <div className="feature-card" key={i}>
                  <div className="feature-card__icon">
                    <Icon size={24} />
                  </div>
                  <h4>{f.title}</h4>
                  <p>{f.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;