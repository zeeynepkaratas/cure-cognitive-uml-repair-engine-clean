# AI Core

## Aciklama

`ai_core`, LangGraph/LangChain tabanli Critic-Healer ajan akisini ve OCL
kurallarini getiren RAG yardimcisini icerir.

## Amac

Hatalari yorumlayan critic ve PlantUML kodunu onaran healer rollerini ayirarak
otonom UML repair akisini desteklemek.

## Kurulum

```bash
pip install -r ai_core/requirements.txt
```

## Konfigurasyon

`ai_core/.env.example` dosyasi kopyalanarak `ai_core/.env` olusturulur.

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

## Kullanim

AI core dogrudan backend tarafindan cagirilir:

```python
UMLMultiAgentSystem(max_iterations=3).run(original_text, initial_uml)
```

## Bagimliliklar

- langchain
- langgraph
- langchain-openai
- python-dotenv
- pydantic

## Dosya Yapisi

- `ai_core/src/ai/agent_workflow.py`
- `ai_core/src/rag/ocl_retriever.py`
- `ai_core/src/llm/`
- `ai_core/log_analiz.py`

## API

Harici HTTP API yoktur. Backend `POST /api/autonomous-repair` bu modulu kullanir.

## Veritabani Degisiklikleri

Yok. RAG kurallari su an bellek icinde tutulur; kalici indeks icin
`data_pipeline/vector_db/` ayrilmistir.

## Test

```bash
python backend/tests/test_api_contracts.py
```

## Hata Senaryolari

- `OPENAI_API_KEY` yoksa backend fallback healer ile devam eder.
- Ajan maksimum 1-3 arasi istek limitine gore calisir.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.0 - AI core dokumantasyonu eklendi.
