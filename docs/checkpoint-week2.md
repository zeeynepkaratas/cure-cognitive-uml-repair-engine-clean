# 📌 Checkpoint — Hafta 2

## Ajanların (Agents) Geliştirilmesi ve RAG Entegrasyonu

- **Hafta:** 2
- **Sprint Hedefi:** Eleştirmen (Critic) ve Onarıcı (Healer) yapay zeka ajanlarını oluşturmak ve RAG altyapısını sisteme entegre etmek

- **Durum:** 🟡 Devam Ediyor
- **Görev Başlangıç Tarihi:** 10.04.2026
- **Görev Bitiş Tarihi:** 20.04.2026
- **Vize haftası sebebiyle 10 gün teslim süresi uygulanmıştır. Checkpoint 3 başlangıç tarihi etkilenmeyecektir.**
------------------------------------------------------------------------

# 🎯 Genel Hedefler

-   [ ] Critic (Eleştirmen) ajanı oluşturuldu
-   [ ] Healer (Onarıcı) ajanı oluşturuldu
-   [ ] Ajanlar arası iletişim mantığı kuruldu
-   [ ] RAG altyapısı kuruldu
-   [ ] Vektör veritabanı hazır
-   [ ] Hata log sistemi çalışıyor
-   [x] Frontend hata gösterim ekranı hazır
-   [ ] JSON hata parser sistemi hazır

------------------------------------------------------------------------

# 👥 Görev Dağılımı ve Detaylı İş Listesi

------------------------------------------------------------------------

# Contributor A

## Sorumluluk: Hata uyarıları ve görsel geri bildirim sistemi oluşturmak

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Hata log ekranı tasarlama | Halüsinasyon ve Design Smell uyarıları | Frontend | ✅ |
| UI hata listesi oluşturma | Hata mesajlarını listeleme | Frontend | ✅ |
| Diyagram hata vurgulama | Hatalı alanları kırmızı renkle gösterme | Frontend | ✅ |
| Tooltip sistemi | Hata detayını hover ile gösterme | Frontend | ✅ |
| Status badge sistemi | Hata türü göstergeleri | Frontend | ✅ |
| Log panel bileşeni | Hata geçmişi ekranı | Frontend | ✅ |
| API hata verisi gösterme | Backend'den gelen JSON'u UI'da gösterme | Frontend | ✅ |
| Responsive tasarım | Mobil uyumlu hata ekranı | Frontend | ✅ |
| Branch yönetimi kontrolü | Feature branch kullanımı | Scrum Master | ✅ |

------------------------------------------------------------------------

# Contributor B

## Sorumluluk: Multi-agent sistemi geliştirmek

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| LangGraph ajan tanımı | Critic node oluşturma | AI Developer | ⬜ |
| Healer ajan tanımı | Onarıcı node oluşturma | AI Developer | ⬜ |
| Ajan mesajlaşma sistemi | Agent-to-agent communication | AI Developer | ⬜ |
| Edge mantığı kodlama | Workflow geçiş kuralları | AI Developer | ⬜ |
| Halüsinasyon tespit promptu | UML doğrulama promptu | AI Developer | ⬜ |
| Onarım promptu | Hatalı UML düzeltme | AI Developer | ⬜ |
| Multi-agent workflow test | Sistem testleri | AI Developer | ⬜ |
| Logging entegrasyonu | Agent çıktı loglama | AI Developer | ⬜ |
| Hata sınıflandırma | Error type categorization | AI Developer | ⬜ |

------------------------------------------------------------------------

# Contributor C

## Sorumluluk: Hata işleme ve doğrulama mekanizmaları

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| JSON parser geliştirme | AI hata raporu ayrıştırma | Backend | ⬜ |
| Error response handler | Hata mesajı işleme | Backend | ⬜ |
| Try-catch mekanizması | Syntax hatalarını yakalama | Backend | ⬜ |
| PlantUML syntax kontrol | UML doğrulama | Backend | ⬜ |
| Error log sistemi | Hata kayıt mekanizması | Backend | ⬜ |
| Exception logging | Runtime hata kaydı | Backend | ⬜ |
| API hata endpoint | /error-log endpoint | Backend | ⬜ |
| Unit test yazımı | Parser testleri | Test | ⬜ |
| Integration test | Agent + API testleri | Test | ⬜ |

------------------------------------------------------------------------

# Contributor D

## Sorumluluk: Vektör veritabanı ve RAG altyapısı

| Görev | Açıklama | Sorumlu | Durum |
| --- | --- | --- | --- |
| Vektör veritabanı kurulumu | FAISS / in-memory rule retrieval prototype | Data Specialist | ⬜ |
| Veri klasörü oluşturma | vector_db dizini | Data Specialist | ⬜ |
| OCL kurallarını chunking | Metin parçalama | Data Specialist | ⬜ |
| Embedding oluşturma | Vektör dönüşümü | Data Specialist | ⬜ |
| Vector index oluşturma | Arama indeksleme | Data Specialist | ⬜ |
| RAG retrieval fonksiyonu | Semantic search | Data Specialist | ⬜ |
| Veri doğrulama testleri | Retrieval accuracy test | Data Specialist | ⬜ |
| Dataset versiyonlama | Veri yönetimi | Data Specialist | ⬜ |
| RAG performans ölçümü | Query latency ölçümü | Data Specialist | ⬜ |

------------------------------------------------------------------------

# 📦 Teknik Teslimatlar (Deliverables)

| Teslimat | Açıklama | Durum |
| --- | --- | --- |
| Critic Agent | Hata tespit sistemi | ⬜ |
| Healer Agent | Otomatik onarım sistemi | ⬜ |
| RAG altyapısı | Vektör arama sistemi | ⬜ |
| Error parser | JSON hata ayrıştırma | ⬜ |
| Log sistemi | Hata kayıt mekanizması | ⬜ |
| UI hata paneli | Frontend hata ekranı | ✅ |

------------------------------------------------------------------------

# 📈 Haftalık Başarı Kriterleri

-   [ ] Critic agent çalışıyor
-   [ ] Healer agent çalışıyor
-   [ ] RAG arama sistemi çalışıyor
-   [x] Hata raporları görüntüleniyor
-   [ ] UML hataları yakalanıyor
-   [ ] Sistem log üretiyor

------------------------------------------------------------------------

# 📝 Notlar

-   Tüm geliştirmeler branch üzerinde yapılacaktır
-   Pull Request zorunludur
-   Kod review yapılmadan merge edilmez
-   Liste görevlerinde `- [x]` / `- [ ]` (gerekirse satıra `⏰` geç teslim, `❌` tamamlanmadı); tablolarda `⬜` / `✅` / `⏰` / `❌` (bkz. `checkpoint-kullanim-rehberi.md`)
