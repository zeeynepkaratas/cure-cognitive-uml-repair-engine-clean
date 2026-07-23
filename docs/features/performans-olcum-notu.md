# Performans Olcum Notu: Tablo IV Latency Kapsami

Bu not, Tablo IV'te raporlanan "50 ardisik analiz istegi" olcumunun hangi
endpoint ve kod yolu uzerinden geldigini aciklar.

## Dogrulanan endpoint

Tablo IV'teki performans olcumu `/api/analyze` endpoint'ine aittir.
`backend/src/api/endpoints.py` icinde `tam_analiz_yap` fonksiyonu su akisi
calistirir:

```python
parse_sonuc = srs_to_plantuml(girdi.metin)
uml = parse_sonuc["plantuml_kodu"]
ocl_sonuc = validate_ocl(uml)
eval_sonuc = calculate_semantic_fidelity(girdi.metin, uml)
```

Bu uc fonksiyonun hicbiri LLM cagrisi yapmaz.

## LLM kullanilmadigina dair import kaniti

`backend/src/parsers/srs_parser.py` yalnizca su importlari yapar:

```python
import re
from typing import Optional
```

`backend/src/ocl_engine/ocl_validator.py` yalnizca su importlari yapar:

```python
import re
from typing import Optional
```

`backend/src/evaluators/semantic_eval.py` yalnizca su importlari yapar:

```python
import re
from typing import Optional
```

Bu dosyalarda `OpenAI`, `ChatOpenAI`, `langchain_openai` veya baska bir LLM
istemcisi import edilmez. Dolayisiyla `/api/analyze` latency degeri regex,
deterministik OCL kontrolu ve deterministik semantik skor hesaplamasini kapsar.

## Yeniden uretilebilir deterministik latency olcumu

Tablo IV kapsamindaki deterministik analiz yuku icin ayrica su betik
eklenmistir:

```text
backend/evaluation/deterministic_analysis_latency_experiment.py
```

Bu betik `/api/analyze` icindeki uc fonksiyonluk is yukunu 50 kez calistirir:

```text
srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity
```

Betik `ChatOpenAI`, `UMLGenerator` veya `UMLMultiAgentSystem` kullanmaz; bu
nedenle LLM API anahtari gerektirmez. 2026-07-06 tarihinde calistirilan son
kosum su dosyalari uretmistir:

```text
backend/evaluation/results/deterministic_analysis_latency_experiment.csv
backend/evaluation/results/deterministic_analysis_latency_experiment.json
backend/evaluation/results/deterministic_analysis_latency_experiment.md
```

Son kosum ozeti:

| Metrik | Deger |
|---|---:|
| Toplam istek | 50 |
| Basarili istek | 50 |
| Ortalama gecikme | 1.054 ms |
| Minimum gecikme | 0.745 ms |
| Maksimum gecikme | 6.796 ms |
| P50 gecikme | 0.824 ms |
| P95 gecikme | 1.629 ms |
| P99 gecikme | 6.796 ms |
| SLA uyum orani | %100.0 |
| LLM cagrisi | 0 |

Bu nedenle onceki 0.4 ms degeri LLM performansi olarak yorumlanmamalidir.
Makale metninde daha guvenli yorum, deterministik `/api/analyze` hattinin
yerel testte milisaniye mertebesinde calistigi; gercek LLM tabanli onarimin
ise ayri olarak `/api/autonomous-repair` deneyleriyle raporlandigidir.

## Gercek LLM tabanli onarim nerede?

Gercek LLM tabanli onarim `/api/autonomous-repair` endpoint'indedir.
`backend/src/api/endpoints.py` icinde baslangic compile testi basarisiz olursa:

```python
agent = UMLMultiAgentSystem(max_iterations=girdi.max_iterations)
aktif_kod = agent.run(original_text=srs_metni, initial_uml=aktif_kod)
```

Bu sinif `ai_core/src/ai/agent_workflow.py` icinde `ChatOpenAI` kullanir:

```python
from langchain_openai import ChatOpenAI
```

Sonuc: Tablo IV'teki `/api/analyze` olcumu gercek LLM onarimini icermez.
LLM latency'si olculmek isteniyorsa `/api/autonomous-repair` icin ayri deney
calistirilmalidir.
