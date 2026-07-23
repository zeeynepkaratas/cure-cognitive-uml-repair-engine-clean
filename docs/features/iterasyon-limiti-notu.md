# Iterasyon Limiti Notu

`UMLMultiAgentSystem` icindeki iterasyon limiti artik sabit `3` degeri yerine
`max_iterations` parametresiyle belirlenir. Backend tarafinda
`/api/autonomous-repair` endpoint'ine gelen `max_iterations` alani da bu
parametreye aktarilir.

## Neden varsayilan limit 3?

Varsayilan deger olan `3`, uc pratik riski dengelemek icin korunmustur:

- Token maliyeti: Her dongude Critic ve gerekirse Healer LLM cagrisi yapar.
  Limit artinca maliyet ve kota kullanimi dogrudan artar.
- Sonsuz veya verimsiz dongu riski: LLM ayni hatayi tekrar uretebilir ya da
  Critic/Healer arasinda ilerleme saglanmadan gidip gelebilir.
- Zaman-performans dengesi: `/api/autonomous-repair` kullaniciya donen bir API
  endpoint'idir. Yuksek limitler basari olasiligini artirabilir, fakat SLA ve
  kullanici bekleme suresi uzerinde dogrudan maliyet olusturur.

## Dikkat edilmesi gereken nokta

Guncel ana repair benchmark kosusu `max_iterations=3` ile yapilmistir:

```bash
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

Limit `2`, `4` ve `5` icin yeni bir duyarlilik analizi yapilmadan
"3 en iyi degerdir" seklinde kesin bir iddia kurulmamali. Makalede daha guvenli
ifade, `max_iterations=3` degerinin bu prototip kosusu icin sabit deney
ayari olarak kullanildigini belirtmektir.
