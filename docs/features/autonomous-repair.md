# Autonomous Repair

## Aciklama

`POST /api/autonomous-repair`, hatali PlantUML kodunu compile/OCL testinden
gecirir, hata varsa AI ajanla veya deterministik fallback healer ile onarim
dener, final compile ve opsiyonel semantik sonucu dondurur.

## Amac

Makaledeki onarim basari oraninin endpoint uzerinden tekrar uretilebilir ve
olculebilir hale gelmesi.

Guncel makale revizyonunda autonomous repair sonucu, deterministic repair ile
ayni `S01`-`S50` ortak benchmark vakalari uzerinde raporlanir.

## Kurulum

```bash
pip install -r backend/requirements.txt
pip install -r ai_core/requirements.txt
```

## Konfigurasyon

`max_iterations` request govdesinden gelir ve 1-5 arasinda sinirlanir.

## Kullanim

```bash
curl -X POST http://localhost:8000/api/autonomous-repair \
  -H "Content-Type: application/json" \
  -d "{\"plantuml_kodu\":\"class UserManager {}\",\"max_iterations\":1}"
```

Ortak benchmark kosusu:

```bash
$env:OPENAI_API_KEY="sk-..."
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

## Bagimliliklar

- Backend compile/OCL validator
- AI core Critic-Healer workflow
- PlantUML renderer

## Dosya Yapisi

- `backend/src/api/endpoints.py`
- `ai_core/src/ai/agent_workflow.py`
- `backend/evaluation/shared_repair_benchmark_cases.py`
- `backend/evaluation/shared_benchmark_llm_experiment.py`

## API

Endpoint: `POST /api/autonomous-repair`

Request:

```json
{
  "plantuml_kodu": "class UserManager {}",
  "srs_metni": "The UserManager handles authentication.",
  "max_iterations": 1
}
```

Response ana alanlari:

```json
{
  "basarili": true,
  "max_iterations": 1,
  "iterasyonlar": [],
  "final_plantuml": "@startuml...",
  "final_compile": {}
}
```

## Veritabani Degisiklikleri

Yok.

## Test

```bash
python backend/tests/test_api_contracts.py
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 1
```

Son ana benchmark sonucu:

| Benchmark | Cases | Successful repairs | Success rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| Shared S01-S50 LLM autonomous repair (`gpt-4o-mini`) | 50 | 47 | 94.0% | 83.8%-97.9% |

## Hata Senaryolari

- AI ajan import edilemezse fallback healer devreye girer.
- Final compile basarisizsa hata log endpointine kayit eklenir.
- `OPENAI_API_KEY` yoksa shared LLM benchmark sonuc uretmeden durur.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.1 - Ortak S01-S50 benchmark sonucu eklendi.
v1.0 - Autonomous repair dokumantasyonu eklendi.
