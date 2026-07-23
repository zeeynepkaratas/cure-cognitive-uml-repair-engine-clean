# Data Pipeline

## Aciklama

Veri hazirlik dosyalari `data_pipeline/` altinda toplandi. Kok dizindeki daginik
CSV ve preprocessing scriptleri ilgili alt klasorlere tasindi.

## Amac

Dataset, preprocessing ve vector DB hazirligi dosyalarini tekrar uretilebilir
bir klasor yapisinda tutmak. Manuel degerlendirme notlari `docs/` altinda
ayri izlenir.

## Kurulum

Ek kurulum yoktur. Scriptler Python standart kutuphaneleri ile calisir.

## Konfigurasyon

Yok.

## Kullanim

```bash
python data_pipeline/preprocessing/xml_to_csv.py
python data_pipeline/preprocessing/cure_veri_hazirlik.py
```

## Bagimliliklar

Mevcut scriptlerin kendi importlari kullanilir.

## Dosya Yapisi

- `data_pipeline/datasets/pure_dataset.csv`
- `data_pipeline/preprocessing/cure_veri_hazirlik.py`
- `data_pipeline/preprocessing/xml_to_csv.py`
- `data_pipeline/vector_db/README.md`
- `docs/ground_truth_manual_review.md`

## API

Yok.

## Veritabani Degisiklikleri

Yok.

## Test

Scriptler kaynak veri ile calistirilip cikti CSV dosyalari kontrol edilir.

## Hata Senaryolari

- Kaynak XML/CSV yoksa script dosya bulunamadi hatasi verir.
- Manuel review tablosu bagimsiz ground truth gibi sunulmamalidir; yalnizca
  sinirli kontrol notu olarak kullanilmalidir.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.0 - Data pipeline klasor yapisi dokumante edildi.
