# 📌 Checkpoint — Hafta 4

## Semantik Skorlama, Akademik Metrikler ve Makale Teslimi

- **Hafta:** 4
- **Sprint Hedefi:** Sistem başarısını bilimsel metriklerle ölçmek, semantik kalite skoru üretmek ve IEEE formatında akademik bildiriyi tamamlayıp teslim etmek
- **Durum:** 🔴 Başlanmadı
- **Görev Başlangıç Tarihi:** 24.04.2026
- **Görev Bitiş Tarihi:** 10.05.2026

------------------------------------------------------------------------

# 🎯 Genel Hedefler

- [ ] Tüm uygulama için son kullanıcı UI/UX testi tamamlandı
- [ ] IEEE şablonunda makale bölümleri birleştirildi ve teslim dosyası hazırlandı
- [ ] LLM-as-a-Judge tabanlı Semantic Fidelity skorlama promptu sisteme eklendi
- [ ] Üretilen UML diyagramları 1-5 arası semantik sadakat puanı alabiliyor
- [ ] E2E hız ve performans testleri tamamlandı
- [ ] API yanıt süresi 15 saniye altında stabilize edildi
- [ ] Onarım loglarından istatistiksel bulgular ve grafikler üretildi
- [ ] İlk üretim hata oranı ve öz-onarım sonrası hata oranı karşılaştırması makaleye eklendi

------------------------------------------------------------------------

# 👥 Görev Dağılımı ve Detaylı İş Listesi

------------------------------------------------------------------------

# Contributor A

## Sorumluluk: Scrum Master + Frontend olarak son kullanıcı testlerini yönetmek ve IEEE makale teslimini tamamlamak

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Son kullanıcı test planı | UI/UX kabul kriterlerini ve test senaryolarını yayınlama | Scrum Master | ⬜ |
| Uygulama akış testi | Dosya yükleme, otonom onarım, final diyagram görüntüleme akışlarını test etme | Frontend | ⬜ |
| UI tutarlılık kontrolü | Formlar, log paneli, progress bileşenleri ve hata mesajlarını doğrulama | Frontend | ⬜ |
| Erişilebilirlik kontrolü | Temel okunabilirlik, kontrast ve mobil kullanılabilirlik denetimi | Frontend | ⬜ |
| Bug triage oturumu | Tespit edilen UI/UX sorunlarını önceliklendirip ekibe dağıtma | Scrum Master | ⬜ |
| Makale bölüm entegrasyonu | Abstract, Introduction, Method, Results bölümlerini tek dokümanda birleştirme | Scrum Master | ⬜ |
| IEEE format son kontrol | Başlık düzeni, referans biçimi, şekil-tablo yerleşimi doğrulama | Scrum Master | ⬜ |
| Son teslim paketi hazırlama | PDF, kaynak dosya ve ek materyal klasörünü düzenleme | Scrum Master | ⬜ |
| Makale teslimi | Son sürümü son tarihte sisteme/kanala yükleme | Scrum Master | ⬜ |

------------------------------------------------------------------------

# Contributor B

## Sorumluluk: Yapay Zeka + NLP olarak Semantic Fidelity skorlama mekanizmasını geliştirmek

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| LLM-as-a-Judge tasarımı | UML semantik doğruluğunu ölçen değerlendirme yaklaşımını tanımlama | AI Developer | ⬜ |
| Skorlama promptu geliştirme | 1-5 arası Semantic Fidelity skoru üreten akademik değerlendirme promptu yazma | NLP | ⬜ |
| Değerlendirme ölçütleri | Doğruluk, tutarlılık, eksiksizlik, OCL uyumu kriterlerini netleştirme | NLP | ⬜ |
| Output şeması standardı | Skor, kısa gerekçe, kritik hata notu alanlarını JSON formatında döndürme | AI Developer | ⬜ |
| Prompt kalibrasyonu | Örnek iyi/kötü UML çıktılarıyla skor dağılımını dengeleme | AI Developer | ⬜ |
| Eşik değer tanımı | Yayınlanacak sonuçlar için kabul edilebilir minimum skor politikasını belirleme | NLP | ⬜ |
| Pipeline entegrasyonu | Final diyagram üretimi sonrası otomatik skorlama adımı ekleme | AI Developer | ⬜ |
| Değerlendirme testleri | Farklı gereksinim metinlerinde skor kararlılığını ölçme | AI Developer | ⬜ |
| Dokümantasyon | Skor metodolojisini Method/Results bölümüne uygun teknik not halinde yazma | NLP | ⬜ |

------------------------------------------------------------------------

# Contributor C

## Sorumluluk: Backend + Test olarak E2E performans testlerini yürütmek ve latency optimizasyonunu tamamlamak

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| E2E test senaryoları | Normal yük, yoğun yük ve hata durumlarını kapsayan uçtan uca testler | Test | ⬜ |
| Performans ölçüm altyapısı | API çağrılarında latency, throughput ve hata oranı ölçümü | Backend | ⬜ |
| 15 sn SLA doğrulama | Yanıt süresinin 15 saniyeyi geçmediğini otomatik kontrol etme | Test | ⬜ |
| Darboğaz analizi | Uzun süren endpoint ve işlem adımlarını profilleme | Backend | ⬜ |
| API optimizasyonu | Gereksiz çağrı azaltma, timeout/retry iyileştirme, cache stratejisi | Backend | ⬜ |
| Asenkron iş akışı düzenleme | Uzun süren adımları kullanıcıyı bloklamadan yönetme | Backend | ⬜ |
| Yük testi raporu | P50/P95/P99 gecikme dağılımlarını raporlama | Test | ⬜ |
| Regresyon testleri | Optimizasyon sonrası işlevsel kırılım kontrolü | Test | ⬜ |
| Final performans raporu | Makaleye girecek performans sonuçlarını tablo halinde sunma | Backend | ⬜ |

------------------------------------------------------------------------

# Contributor D

## Sorumluluk: Veri Uzmanı + Database olarak onarım loglarını analiz edip akademik bulgulara dönüştürmek

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Log veri çekimi | Veritabanından tüm iterasyon/onarım kayıtlarını çıkarma | Database | ⬜ |
| Veri temizleme ve doğrulama | Eksik, tutarsız ve mükerrer kayıtları ayıklama | Data Specialist | ⬜ |
| İlk üretim hata oranı hesabı | Onarım öncesi hata yoğunluğunu istatistiksel olarak hesaplama | Data Specialist | ⬜ |
| Öz-onarım sonrası hata oranı | Onarım sonrası kalan hata oranını ölçme | Data Specialist | ⬜ |
| Karşılaştırmalı analiz | Öncesi-sonrası hata oranı farkını yüzdesel iyileşme ile raporlama | Data Specialist | ⬜ |
| İstatistiksel tablo üretimi | Makaleye uygun sonuç tablolarını oluşturma | Data Specialist | ⬜ |
| Başarı grafikleri | İterasyon sayısı, başarı oranı ve düzelme trendi grafikleri üretme | Data Specialist | ⬜ |
| Sonuç paketleme | Tablo ve grafik setini standart isimlendirme ile teslim etme | Database | ⬜ |
| Scrum Master teslimi | Makale entegrasyonu için bulguları zamanında paylaşma | Data Specialist | ⬜ |

------------------------------------------------------------------------

# 📦 Teknik Teslimatlar (Deliverables)

| Teslimat | Açıklama | Durum |
| --- | --- | --- |
| UI/UX son kullanıcı test raporu | Son sürüm arayüz kullanılabilirlik değerlendirmesi | ⬜ |
| IEEE format akademik bildiri | Abstract, Intro, Method, Results bölümleri tamamlanmış teslim dosyası | ⬜ |
| Semantic Fidelity skorlama modülü | LLM-as-a-Judge tabanlı 1-5 semantik sadakat puanlayıcı | ⬜ |
| E2E performans raporu | Hız, gecikme ve dayanıklılık sonuçları | ⬜ |
| API optimizasyon çıktıları | 15 saniye altı yanıt süresi için iyileştirilmiş çağrı akışı | ⬜ |
| İstatistiksel bulgu seti | Hata oranı karşılaştırma tabloları ve başarı grafikleri | ⬜ |

------------------------------------------------------------------------

# 📈 Haftalık Başarı Kriterleri

- [ ] Son kullanıcı test senaryolarının tamamı uygulanmış ve raporlanmış
- [ ] Makale IEEE formatına uygun şekilde yazılıp teslime hazır hale getirilmiş
- [ ] Sistem her final UML için 1-5 aralığında Semantic Fidelity skoru üretiyor
- [ ] Skorlama çıktısı gerekçeli ve tekrar edilebilir sonuç veriyor
- [ ] E2E testlerde sistem yanıt süresi 15 saniyenin altında tutuluyor
- [ ] Optimizasyon sonrası performans regresyonu bulunmuyor
- [ ] İlk üretim ve öz-onarım sonrası hata oranı karşılaştırmalı olarak raporlanmış
- [ ] Grafik ve tablolar makaleye entegre edilecek kaliteye ulaşmış

------------------------------------------------------------------------

# 📝 Notlar

- Tüm geliştirmeler branch üzerinde yapılacaktır
- Pull Request zorunludur
- Kod review yapılmadan merge edilmez
- Liste görevlerinde `- [x]` / `- [ ]` (gerekirse satıra `⏰` geç teslim, `❌` tamamlanmadı); tablolarda `⬜` / `✅` / `⏰` / `❌` (bkz. `checkpoint-kullanim-rehberi.md`)
