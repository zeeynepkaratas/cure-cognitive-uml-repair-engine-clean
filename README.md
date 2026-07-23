# CURE - Cognitive UML Repair Engine

CURE, yazılım gereksinim metinlerinden UML sınıf diyagramı üreten, diyagramı OCL benzeri kurallarla doğrulayan, semantik sadakatini ölçen ve gerektiğinde çoklu ajan tabanlı onarım akışıyla düzeltmeye çalışan bir araştırma ve prototip sistemidir.

Proje üç ana parçadan oluşur:

- `backend`: FastAPI tabanlı API servisi.
- `frontend`: React + Vite tabanlı web arayüzü.
- `ai_core`: LangGraph/LangChain tabanlı Critic-Healer ajan akışı ve RAG destekli OCL kural getirme modülü.

## İçindekiler

- [Özellikler](#özellikler)
- [Mimari](#mimari)
- [Klasör Yapısı](#klasör-yapısı)
- [Kurulum](#kurulum)
- [Çalıştırma](#çalıştırma)
- [API Uçları](#api-uçları)
- [Frontend Kullanımı](#frontend-kullanımı)
- [Testler](#testler)
- [Repair Benchmark Results](#repair-benchmark-results)
- [Veri Hazırlık Araçları](#veri-hazırlık-araçları)
- [Ortam Değişkenleri](#ortam-değişkenleri)
- [Geliştirme Kuralları](#geliştirme-kuralları)

## Özellikler

- SRS metninden PlantUML sınıf diyagramı üretimi.
- Sınıf ve ilişki çıkarımı için kural tabanlı parser.
- PlantUML syntax ön kontrolü.
- OCL benzeri doğrulama kuralları:
  - `@startuml` ve `@enduml` kontrolü.
  - En az bir sınıf zorunluluğu.
  - PascalCase sınıf adı kontrolü.
  - God Class uyarısı.
  - İzole sınıf tespiti.
  - Döngüsel bağımlılık tespiti.
  - Tekrarlanan sınıf adı tespiti.
  - Diyagram karmaşıklığı uyarısı.
- IEEE/ISO 29148 yaklaşımına dayalı semantik sadakat skoru.
- SVG tabanlı offline UML önizleme üretimi.
- PNG data URI çıktısı ile frontend sözleşmesi uyumluluğu.
- Çoklu ajan tabanlı otonom onarım akışı:
  - Critic ajanı hataları bulur.
  - Healer ajanı PlantUML kodunu düzeltir.
  - En fazla 3 iterasyonla döngü sınırlandırılır.
- In-memory hata log sistemi.
- P50/P95/P99 ve SLA odaklı performans raporu.
- React arayüzünde analiz, sonuç görüntüleme ve onarım sayfaları.

## Mimari

Temel veri akışı şöyledir:

```text
SRS Metni
   |
   v
SRS Parser
   |
   v
PlantUML Üretimi
   |
   +--> SVG Render
   |
   +--> OCL Doğrulama
   |
   +--> Semantik Sadakat Analizi
   |
   v
Sonuç Ekranı
   |
   v
Gerekirse Otonom Onarım
   |
   v
Critic -> Healer -> Compile Test -> Final UML
```

Ana backend giriş noktası:

```text
backend/src/api/endpoints.py
```

Frontend API istemcisi:

```text
frontend/src/services/api.js
```

AI ajan akışı:

```text
ai_core/src/ai/agent_workflow.py
```

## Klasör Yapısı

```text
.
├── ai_core/
│   ├── README.md
│   ├── requirements.txt
│   └── src/
│       ├── ai/
│       │   └── agent_workflow.py
│       ├── llm/
│       │   ├── semantic_evaluator.py
│       │   └── uml_generator.py
│       └── rag/
│           └── ocl_retriever.py
├── backend/
│   ├── requirements.txt
│   ├── src/
│   │   ├── api/
│   │   │   ├── endpoints.py
│   │   │   ├── error_log_endpoint.py
│   │   │   └── performance.py
│   │   ├── evaluators/
│   │   │   └── semantic_eval.py
│   │   ├── ocl_engine/
│   │   │   ├── error_handler.py
│   │   │   └── ocl_validator.py
│   │   ├── parsers/
│   │   │   └── srs_parser.py
│   │   └── renderers/
│   │       └── plantuml_renderer.py
│   └── tests/
│       ├── test_backend.py
│       ├── test_full.py
│       └── test_api_contracts.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── components/
│       ├── context/
│       ├── pages/
│       └── services/
├── docs/
│   ├── checkpoint-week1.md
│   ├── checkpoint-week2.md
│   ├── checkpoint-week3.md
│   ├── checkpoint-week4.md
│   ├── checkpoint-kullanim-rehberi.md
│   └── features/
├── data_pipeline/
│   ├── datasets/
│   │   └── pure_dataset.csv
│   ├── preprocessing/
│   │   ├── cure_veri_hazirlik.py
│   │   └── xml_to_csv.py
│   └── vector_db/
├── docs/
│   └── ground_truth_manual_review.md
├── experiments/
│   └── run_autonomous_repair.py
└── results/
```

## Kurulum

### Gereksinimler

- Python 3.10 veya üzeri.
- Node.js 20 veya üzeri.
- npm.
- Otonom AI onarım akışı için OpenAI API anahtarı.

Backend ve AI modülleri ayrı `requirements.txt` dosyalarına sahiptir. Temel backend akışı AI paketleri olmadan da çalışabilir; ancak `/api/autonomous-repair` endpointinin gerçek ajan akışını kullanabilmesi için `ai_core` bağımlılıkları ve API anahtarı gerekir.

### Depoyu Klonlama

```bash
git clone <ANONYMIZED_REPOSITORY_URL>
cd cure-cognitive-uml-repair-engine
```

### Backend Kurulumu

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r ..\ai_core\requirements.txt
```

macOS/Linux:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r ../ai_core/requirements.txt
```

### Frontend Kurulumu

```bash
cd frontend
npm install
```

## Çalıştırma

### Backend

Backend servisini repo kökünden çalıştırmak önerilir:

```bash
uvicorn backend.src.api.endpoints:app --reload --host 0.0.0.0 --port 8000
```

Alternatif olarak `backend` klasöründeyken:

```bash
uvicorn src.api.endpoints:app --reload --host 0.0.0.0 --port 8000
```

Servis ayaktayken:

- API kökü: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Sağlık kontrolü: `http://localhost:8000/health`
- Demo diyagram: `http://localhost:8000/api/demo-diagram`

### Frontend

```bash
cd frontend
npm run dev
```

Vite varsayılan olarak uygulamayı şu adreste açar:

```text
http://localhost:5173
```

Frontend varsayılan API adresi:

```text
http://localhost:8000
```

Gerekirse `frontend/.env.local` içinde değiştirilebilir:

```env
VITE_API_URL=http://localhost:8000
```

## API Uçları

### Genel

| Yöntem | Yol | Açıklama |
|---|---|---|
| `GET` | `/` | Servis bilgisi ve endpoint listesi. |
| `GET` | `/health` | Backend sağlık kontrolü. |
| `GET` | `/api/demo-diagram` | Tarayıcıda doğrudan SVG UML demo sayfası. |

### SRS ve UML İşlemleri

| Yöntem | Yol | Açıklama |
|---|---|---|
| `POST` | `/generate-uml` | CP1 uyumluluk endpointi. `/api/parse` akışını kullanır. |
| `POST` | `/api/parse` | SRS metninden PlantUML üretir, render ve OCL doğrulama sonucu döner. |
| `POST` | `/api/render` | PlantUML kodunu SVG/PNG response formatına çevirir. |
| `POST` | `/api/validate` | PlantUML kodunu OCL kurallarına göre doğrular. |
| `POST` | `/api/evaluate` | SRS metni ile PlantUML kodunun semantik sadakatini ölçer. |
| `POST` | `/api/analyze` | Tam pipeline: SRS -> UML -> OCL -> semantik analiz. |
| `POST` | `/api/iterate` | Tek onarım iterasyonu için compile ve opsiyonel semantik test çalıştırır. |
| `POST` | `/api/autonomous-repair` | Çoklu ajan destekli otonom UML onarım akışını çalıştırır. |

### Hata Logları

| Yöntem | Yol | Açıklama |
|---|---|---|
| `POST` | `/api/error-log` | Hata kaydı oluşturur. |
| `GET` | `/api/error-log` | Hata kayıtlarını listeler. `kategori` ve `son_n` parametrelerini destekler. |
| `DELETE` | `/api/error-log` | In-memory hata kayıtlarını temizler. |

### Performans

| Yöntem | Yol | Açıklama |
|---|---|---|
| `POST` | `/api/performance/measure` | Manuel performans ölçümü kaydeder. |
| `GET` | `/api/performance` | P50/P95/P99, başarı oranı ve SLA raporu döner. |
| `DELETE` | `/api/performance` | Performans ölçümlerini temizler. |

### Örnek İstekler

SRS analiz:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{\"metin\":\"The UserManager handles user authentication. The DiagramService generates PlantUML diagrams. The UserManager uses the DiagramService.\",\"dil\":\"en\"}"
```

PlantUML doğrulama:

```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d "{\"plantuml_kodu\":\"@startuml\nclass UserManager {}\n@enduml\"}"
```

Otonom onarım:

```bash
curl -X POST http://localhost:8000/api/autonomous-repair \
  -H "Content-Type: application/json" \
  -d "{\"plantuml_kodu\":\"class UserManager {}\",\"max_iterations\":3}"
```

## Frontend Kullanımı

Arayüz üç ana sayfadan oluşur:

- `HomePage`: SRS dosyası yükleme ve analiz başlatma.
- `ResultsPage`: Üretilen UML, OCL sonucu, semantik skor, sınıflar ve ilişkiler.
- `RepairPage`: Otonom onarım süreci, iterasyon zaman çizelgesi ve final UML çıktısı.

Desteklenen dosya türleri:

| Alan | Türler | Zorunlu mu |
|---|---|---|
| SRS Belgesi | `.txt`, `.pdf` | Evet |
| Mevcut UML | `.xmi`, `.uml`, `.puml`, `.plantuml` | Hayır |

## Testler

Backend tarafındaki kapsamlı test paketi:

```bash
python backend/tests/test_full.py
```

Bu test paketi şunları kapsar:

- JSON hata parser testleri.
- Syntax kontrol testleri.
- OCL doğrulama testleri.
- İterasyon simülasyonu.
- SRS -> UML -> OCL -> semantik E2E akışı.
- Performans ve SLA kontrolleri.
- Regresyon kontrolleri.

API kontrat testleri:

```bash
python backend/tests/test_api_contracts.py
```

Bu dosya `fastapi` ortamda kurulu değilse kendini güvenli şekilde `SKIP` eder.

Frontend kontrolleri:

```bash
cd frontend
npm run lint
npm run build
```

## Repair Benchmark Results

The current paper revision reports repair performance on a shared benchmark of
50 invalid PlantUML scenarios (`S01`-`S50`). Deterministic repair and the real
LLM-based autonomous repair endpoint are evaluated on the same cases, with
`max_iterations=3`.

| Repair mode | Cases | Successful repairs | Success rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| Deterministic backend repair | 50 | 31 | 62.0% | 48.2%-74.1% |
| LLM autonomous repair (`gpt-4o-mini`) | 50 | 47 | 94.0% | 83.8%-97.9% |

Primary benchmark files:

```text
backend/evaluation/shared_repair_benchmark_cases.py
backend/evaluation/shared_benchmark_deterministic_experiment.py
backend/evaluation/shared_benchmark_llm_experiment.py
backend/evaluation/results/shared_benchmark_deterministic_experiment.*
backend/evaluation/results/shared_benchmark_llm_experiment.*
```

Reproduce the deterministic benchmark:

```bash
python backend/evaluation/shared_benchmark_deterministic_experiment.py
```

Reproduce the LLM benchmark:

```bash
$env:OPENAI_API_KEY="sk-..."
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

The older 20-case deterministic smoke-test script is retained only for helper
functions and backward-compatible development checks. The old autonomous repair
experiment files were removed; they are not the main paper evidence for the
current revision.

## Veri Hazırlık Araçları

Veri hazırlık dosyaları `data_pipeline/` altında toplanmıştır:

- `data_pipeline/preprocessing/xml_to_csv.py`: XML tabanlı veri kaynaklarını CSV formatına dönüştürmek için kullanılır.
- `data_pipeline/preprocessing/cure_veri_hazirlik.py`: CURE veri hazırlık akışında kullanılan yardımcı script.

Ana veri dosyası:

```text
data_pipeline/datasets/pure_dataset.csv
```

Güncel ortak onarım benchmarklarını tekrar üretmek için:

```bash
python backend/evaluation/shared_benchmark_deterministic_experiment.py
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

## Ortam Değişkenleri

### Frontend

`frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

### AI Core

Otonom ajan akışı `langchain-openai` kullandığı için OpenAI API anahtarı gerekir.

PowerShell:

```powershell
$env:OPENAI_API_KEY="sk-..."
```

macOS/Linux:

```bash
export OPENAI_API_KEY="sk-..."
```

Kalıcı kullanım için `.env` dosyası tercih edilebilir. Gizli anahtarlar repoya commit edilmemelidir.

## Geliştirme Kuralları

Projede dokümantasyon ve checkpoint disiplini önemlidir.

- Yeni özellikler için `docs/features/` altında dokümantasyon eklenmelidir.
- Teknik değişiklikler test edilmeden tamamlanmış sayılmamalıdır.
- Backend endpoint değişiklikleri frontend API istemcisiyle birlikte kontrol edilmelidir.
- Yeni bağımlılıklar ilgili `requirements.txt` veya `package.json` dosyasına eklenmelidir.
- Ana branch üzerinde doğrudan çalışma yerine feature branch ve pull request akışı kullanılmalıdır.
- Checkpoint dosyaları güncellenirken `docs/checkpoint-kullanim-rehberi.md` takip edilmelidir.

## Örnek Tam Geliştirme Akışı

1. Backend'i başlat:

   ```bash
   uvicorn backend.src.api.endpoints:app --reload --port 8000
   ```

2. Frontend'i başlat:

   ```bash
   cd frontend
   npm run dev
   ```

3. Tarayıcıdan arayüzü aç:

   ```text
   http://localhost:5173
   ```

4. SRS metni içeren `.txt` dosyası yükle.

5. Analizi başlat.

6. Sonuç ekranında UML diyagramını, OCL skorunu ve semantik skoru kontrol et.

7. Hata varsa onarım ekranına geç.

8. Final PlantUML veya SVG çıktısını indir.

## Proje Durumu

Bu repo, CURE projesinin güncel prototip uygulamasını içerir. Backend test paketi, temel parser/doğrulama/semantik analiz ve performans akışlarının çalıştığını doğrulamak için hazırlanmıştır. Sistem akademik geliştirme, sprint teslimleri ve demo amaçlı kullanılabilecek şekilde düzenlenmiştir.
