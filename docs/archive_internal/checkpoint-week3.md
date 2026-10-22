# 📌 Checkpoint — Hafta 3

## Otonom "Dene-Onar-Tekrarla" Döngüsünün Kodlanması

- **Hafta:** 3
- **Sprint Hedefi:** Sistemin insan müdahalesi olmadan hatayı tespit edip onarması, iterasyon sürecinin görünür hale getirilmesi ve sonsuz döngülerin engellenmesi
- **Durum:** 🟡 Devam Ediyor
- **Görev Başlangıç Tarihi:** 17.04.2026
- **Görev Bitiş Tarihi:** 24.04.2026

------------------------------------------------------------------------

# 🎯 Genel Hedefler

- [ ] Arayüze "Otonom Onarım İşlemi" progress bar eklendi
- [ ] Arayüzde iterasyon bazlı log akış ekranı tamamlandı
- [ ] Critic ajanı RAG üzerinden OCL kurallarını çekiyor
- [ ] Critic hata bulduğunda Healer ajana otomatik aktarım yapılıyor
- [ ] LangGraph workflow'unda maksimum 3 iterasyon limiti aktif
- [ ] Backend her onarım adımında anlık compile test çalıştırıyor
- [ ] Otonom onarım başarılıysa final diyagram frontend'e gönderiliyor
- [ ] Her iterasyon log analytics olarak veritabanına kaydediliyor

------------------------------------------------------------------------

# 👥 Görev Dağılımı ve Detaylı İş Listesi

------------------------------------------------------------------------

# Contributor A

## Sorumluluk: Scrum Master + Frontend olarak otonom onarım sürecinin UI takibini ve sprint koordinasyonunu yürütmek

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Sprint planı netleştirme | Hafta 3 kapsamı ve acceptance criteria kilitleme | Scrum Master | ✅ |
| Otonom onarım progress bar | Iterasyon ilerlemesini yüzde ve adım bazlı gösterme | Frontend | ✅ |
| Progress durum etiketleri | `Analiz`, `Onarım`, `Derleme Testi`, `Tamamlandı` adımlarını görselleştirme | Frontend | ✅ |
| Log akış paneli tasarımı | Sistemin her denemesini kronolojik timeline olarak gösterme | Frontend | ✅ |
| Iterasyon kart bileşeni | Her deneme için hata tipi, düzeltme özeti, compile sonucu gösterme | Frontend | ✅ |
| Canlı durum güncellemesi | Backend stream/polling ile ekranın anlık güncellenmesi | Frontend | ✅ |
| Başarı/başarısızlık görsel dili | 3 deneme sonrası başarısızlık veya başarı durumlarını ayırt etme | Frontend | ✅ |
| Kullanıcı bilgilendirme metinleri | Otonom süreçte kullanıcıya "bekle", "incele", "tamamlandı" mesajları | Frontend | ✅ |
| Günlük scrum takip notu | Ekip ilerleme-gelinen engel-kapanan risk kayıtları | Scrum Master | ⬜ |

------------------------------------------------------------------------

# Contributor B

## Sorumluluk: Yapay Zeka + NLP olarak Critic-Healer otonom döngüsünü ve iterasyon limitini kodlamak

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Critic RAG sorgu akışı | OCL kural setini vektör arama ile bağlama | AI Developer | ⬜ |
| OCL retrieval doğrulama | Gelen kural parçalarının bağlama uygunluğunu kontrol etme | NLP | ⬜ |
| Critic hata tespit promptu güncelleme | OCL ihlali ve UML tasarım hatasını ayrıştırma | AI Developer | ⬜ |
| Critic-Healer veri kontratı | Hata çıktısının Healer tarafından tüketilebilir JSON formatına çevrilmesi | AI Developer | ⬜ |
| Healer onarım çağrısı | Hata bulunduğunda otomatik düzeltme ajanının tetiklenmesi | AI Developer | ⬜ |
| LangGraph state güncellemesi | Her iterasyonda state'e deneme sayısı ve sonuç yazma | AI Developer | ⬜ |
| Maksimum 3 iterasyon limiti | `max_iteration = 3` guard koşulu ve stop node tanımlama | NLP | ⬜ |
| Döngü kırma senaryoları | Aynı hatanın tekrar ettiği durumda erken sonlandırma kuralı | NLP | ⬜ |
| Otonom döngü test senaryoları | 1. denemede başarı, 3. denemede başarı, 3 denemede başarısızlık akışlarını test etme | AI Developer | ⬜ |

------------------------------------------------------------------------

# Contributor C

## Sorumluluk: Backend + Test olarak anlık compile testlerini ve final diyagram teslim akışını tamamlamak

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Compile test servisi | Healer çıktısını her iterasyonda otomatik derleme/syntax testine sokma | Backend | ⬜ |
| Iterasyon başına test endpointi | Her deneme sonucunu API üzerinden durum kodu ile döndürme | Backend | ⬜ |
| Compile hata normalize etme | Farklı hata tiplerini standart response modeline çevirme | Backend | ⬜ |
| Otonom işlem orkestrasyonu | Critic-Healer-Compile adımlarını tek akışta koordine etme | Backend | ⬜ |
| Başarılı onarım sonrası final üretim | Son geçerli UML/diagram çıktısını finalize etme | Backend | ⬜ |
| Frontend final gönderim akışı | Başarı sonrası final diyagramı UI'a iletme endpointi | Backend | ⬜ |
| Retry ve timeout yönetimi | Iterasyon başına süre sınırı ve güvenli tekrar politikası | Backend | ⬜ |
| Unit testler | Compile servisleri ve response mapper fonksiyonlarının testi | Test | ⬜ |
| Integration testler | Uçtan uca otonom döngü + final diyagram tesliminin testi | Test | ⬜ |

------------------------------------------------------------------------

# Contributor D

## Sorumluluk: Veri Uzmanı + Database olarak iterasyon log analytics verisini kalıcı hale getirmek

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Iterasyon log şeması tasarımı | `run_id`, `iteration_no`, `error_type`, `fix_status`, `compile_result` alanlarını modelleme | Data Specialist | ⬜ |
| Log tablosu oluşturma | Otonom döngü için analytics odaklı DB tablosu açma | Database | ⬜ |
| Olay bazlı kayıt mekanizması | Her Critic-Healer-Compile adımını zaman damgası ile kaydetme | Database | ⬜ |
| Hata sınıflandırma kaydı | Bulunan hata kategorilerini analiz için normalize etme | Data Specialist | ⬜ |
| Kaçıncı denemede düzeldi metriği | Çözüm iterasyonunu ayrı metrik alanında tutma | Data Specialist | ⬜ |
| Başarı oranı hesaplama sorguları | 1/2/3. denemede başarı dağılımını raporlama | Data Specialist | ⬜ |
| Makale bulguları için export | CSV/JSON çıktı ile "Bulgular" bölümüne veri hazırlama | Data Specialist | ⬜ |
| Veri doğrulama testleri | Eksik kayıt, çift kayıt ve sıra bozulması kontrolleri | Database | ⬜ |
| Log retention politikası | Analiz dönemi boyunca logların güvenli saklanması | Database | ⬜ |

------------------------------------------------------------------------

# 📦 Teknik Teslimatlar (Deliverables)

| Teslimat | Açıklama | Durum |
| --- | --- | --- |
| Otonom onarım progress bar | Iterasyon ilerleme göstergesi | ⬜ |
| Log akış ekranı | Adım adım self-repair timeline | ⬜ |
| Critic RAG + OCL entegrasyonu | Kural çekme ve hata tespit katmanı | ⬜ |
| LangGraph iterasyon limiti | Maksimum 3 denemede güvenli durdurma | ⬜ |
| Compile test pipeline | Her onarım sonrası otomatik derleme kontrolü | ⬜ |
| Final diyagram teslim akışı | Başarılı onarımın frontend'e aktarımı | ⬜ |
| Iterasyon log analytics veritabanı | Bulgular için kalıcı ölçüm verisi | ⬜ |

------------------------------------------------------------------------

# 📈 Haftalık Başarı Kriterleri

- [ ] Kullanıcı otonom onarım sürecini progress bar üzerinden canlı izleyebiliyor
- [ ] Log panelinde en az 3 iterasyonun adım bazlı çıktısı görülebiliyor
- [ ] Critic ajanı OCL kuralını RAG ile çekip ihlali tespit edebiliyor
- [ ] Hata bulunduğunda Healer ajanı otomatik devreye giriyor
- [ ] LangGraph akışı 3 iterasyonda güvenli şekilde duruyor
- [ ] Backend her iterasyonda compile test sonucu üretiyor
- [ ] Başarılı durumda final diyagram frontend'e otomatik iletiliyor
- [ ] Iterasyon kayıtları veritabanında analiz edilebilir biçimde tutuluyor

------------------------------------------------------------------------

# 📝 Notlar

- Tüm geliştirmeler branch üzerinde yapılacaktır
- Pull Request zorunludur
- Kod review yapılmadan merge edilmez
- Liste görevlerinde `- [x]` / `- [ ]` (gerekirse satıra `⏰` geç teslim, `❌` tamamlanmadı); tablolarda `⬜` / `✅` / `⏰` / `❌` (bkz. `checkpoint-kullanim-rehberi.md`)
