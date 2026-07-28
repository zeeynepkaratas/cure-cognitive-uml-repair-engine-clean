# Data Pipeline

Bu klasor, CURE veri hazirlik akislarini kok dizinden ayirir.

- `datasets/`: Ham veya hazirlanmis veri dosyalari.
- `preprocessing/`: XML/CSV donusumu ve veri temizleme scriptleri.
- `vector_db/`: RAG/OCL kural indeksleri icin hazirlik notlari.

Manuel kontrol notlari data pipeline altinda tutulmaz. Sınırlı elle inceleme
tablosu icin `docs/ground_truth_manual_review.md` dosyasina bakilmalidir.

Kok dizindeki eski veri dosyalari ve `xml_to_csv.py` donusum scripti bu yapi
altina tasinmistir. Raporlanan deneylerde kullanilmayan eski yardimci
vektor-indeks hazirlik scripti temiz kaynak paketinden cikarilmistir.
