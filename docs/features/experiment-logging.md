# Experiment Logging

## Aciklama

Guncel deney protokolu, deterministic repair ve gercek LLM tabanli autonomous
repair akisini ayni `S01`-`S50` PlantUML benchmark vakalari uzerinde calistirir.
Sonuclar `backend/evaluation/results/` altina CSV/JSON/MD olarak yazilir.

## Amac

Basari orani gibi makale metriklerini elle yazilmis dosyalara dayandirmadan,
tekrar uretilebilir ve ortak veri setine dayali deney ciktilariyla hesaplamak.

## Kurulum

```bash
pip install -r backend/requirements.txt
pip install -r ai_core/requirements.txt
```

## Konfigurasyon

Deterministik repair:

```bash
python backend/evaluation/shared_benchmark_deterministic_experiment.py
```

LLM autonomous repair:

```bash
$env:OPENAI_API_KEY="sk-..."
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

## Kullanim

```bash
python backend/evaluation/shared_benchmark_deterministic_experiment.py
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

Son ana kosu sonuclari:

| Repair mode | Cases | Successful repairs | Success rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| Deterministic backend repair | 50 | 31 | 62.0% | 48.2%-74.1% |
| LLM autonomous repair (`gpt-4o-mini`) | 50 | 47 | 94.0% | 83.8%-97.9% |

## Bagimliliklar

- Backend deterministic repair helpers
- Backend autonomous repair endpoint fonksiyonu
- AI core Critic-Healer workflow
- Python csv/json standart kutuphaneleri

## Dosya Yapisi

- `backend/evaluation/shared_repair_benchmark_cases.py`
- `backend/evaluation/shared_benchmark_deterministic_experiment.py`
- `backend/evaluation/shared_benchmark_llm_experiment.py`
- `backend/evaluation/results/shared_benchmark_deterministic_experiment.*`
- `backend/evaluation/results/shared_benchmark_llm_experiment.*`

## API

Scriptler backend fonksiyonlarini process icinde cagirir. Calisan HTTP sunucu gerekmez.

## Veritabani Degisiklikleri

Yok.

## Test

```bash
python backend/evaluation/shared_benchmark_deterministic_experiment.py
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 1
```

## Hata Senaryolari

- `OPENAI_API_KEY` yoksa LLM benchmark sonuc uretmeden durur.
- LLM benchmark tamamlanmadan kesilirse `.partial.csv` ve `.partial.json` ara kayitlari olusur; bunlar makale sonucu olarak raporlanmaz.
- Output klasoru yoksa script otomatik olusturur.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.1 - Ortak S01-S50 repair benchmark protokolu ve 31/50, 47/50 sonuclari eklendi.
v1.0 - Deney loglama dokumantasyonu eklendi.
