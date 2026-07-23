# AI Core: Cognitive UML Repair Engine (CURE)

Bu dizin, **CURE (Cognitive UML Repair Engine)** projesinin kalbi olan yapay zeka ve NLP süreçlerini barındırmaktadır. Sistem, ham gereksinim metinlerinden PlantUML diyagramları üretmek, bunları otonom bir şekilde denetlemek ve semantik sadakat skorlaması yapmak üzere tasarlanmış çoklu-ajan (multi-agent) bir mimariye sahiptir.

## 🏗 Mimari Yapı

`ai_core`, LangGraph üzerine inşa edilmiş bir **Critic-Healer (Eleştirmen-Onarıcı)** döngüsünü temel alır. Bu döngü, üretilen UML diyagramlarının hem sözdizimsel (syntactic) hem de anlamsal (semantic) olarak doğruluğunu garanti eder.

### Klasör Yapısı
```text
ai_core/
├── src/
│   ├── ai/                 # LangGraph Ajan Mimarisi (Critic & Healer)
│   │   └── agent_workflow.py
│   ├── rag/                # RAG Altyapısı (OCL Kısıt Kuralları)
│   │   └── ocl_retriever.py
│   └── llm/                # Model Bağlantıları & Değerlendirme Modülleri
│       ├── uml_generator.py
│       └── semantic_evaluator.py
├── .env                    # API Anahtarları ve Yapılandırma
├── requirements.txt        # Bağımlılıklar (LangChain, LangGraph, FAISS vb.)
└── README.md               # Teknik Dokümantasyon

🛠 Kurulum ve Kullanım
1. Ortam Kurulumu
Öncelikle bir sanal ortam oluşturun ve bağımlılıkları yükleyin:
cd ai_core
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
pip install -r requirements.txt

2. Yapılandırma
.env dosyasını oluşturun ve API anahtarınızı ekleyin:

OPENAI_API_KEY=your_api_key_here

3. Çalıştırma
Otonom döngüyü başlatmak için:

python -m src.ai.agent_workflow

📊 Skorlama Metodolojisi (LLM-as-a-Judge)
Üretilen diyagramlar şu kriterlere göre değerlendirilir:

Doğruluk: Metindeki nesnelerin ve niteliklerin doğru aktarımı.

Tutarlılık: İlişki yönlerinin ve türlerinin mantıksal bütünlüğü.

OCL Uyumu: Vektör tabanından gelen iş kurallarına sadakat.

## Repair Benchmark Evidence

Current repair evaluation uses a shared benchmark of 50 invalid PlantUML cases
(`S01`-`S50`). Both deterministic backend repair and the real LLM-based
autonomous repair endpoint are evaluated on the same cases with
`max_iterations=3`.

| Repair mode | Cases | Successful repairs | Success rate |
|---|---:|---:|---:|
| Deterministic backend repair | 50 | 31 | 62.0% |
| LLM autonomous repair (`gpt-4o-mini`) | 50 | 47 | 94.0% |

Primary evidence files are under `backend/evaluation/shared_*` and
`backend/evaluation/results/shared_benchmark_*`.
