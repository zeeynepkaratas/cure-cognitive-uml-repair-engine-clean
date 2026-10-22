# 📌 Checkpoint — Hafta 1

## Altyapı Kurulumu, Ortam Hazırlığı ve Temel Üretim

- **Hafta:** 1
- **Sprint Hedefi:** Sistemin temel iskeletini ayağa kaldırmak ve ham metinden ilk UML çıktısını üretmek
- **Durum:** 🟢 Tamamlandı (eksiklerle; bazı görevler ❌/⬜)
- **Görev Başlangıç Tarihi:** 03.04.2026
- **Görev Bitiş Tarihi:** 10.04.2026

---

# 🎯 Genel Hedefler

- [x] Proje repository oluşturuldu
- [x] Branch yönetim kuralları belirlendi
- [x] Frontend temel arayüz hazır
- [ ] Backend API çalışır durumda
- [ ] LLM bağlantısı kuruldu
- [ ] PlantUML render sistemi entegre edildi
- [X] Test veri seti hazırlandı
- [ ] OCL ve UML standart dokümanları toplandı

---

# 👥 Görev Dağılımı ve Detaylı İş Listesi

---

#  Contributor A

## Sorumluluk: Web arayüzü altyapısını kurmak ve kullanıcı giriş ekranını oluşturmak

| Görev                       | Açıklama                                    | Sorumlu      | Durum |
| --------------------------- | ------------------------------------------- | ------------ | ----- |
| Proje repository oluşturma  | GitHub üzerinde ana proje oluşturulacak     | Scrum Master | ✅   |
| Branch stratejisi belirleme | main / isim-soyisim yapısı kurulacak        | Scrum Master | ✅   |
| Branch koruma kuralları     | PR zorunlu olacak                           | Scrum Master | ✅   |
| Frontend framework kurulumu | React veya Vue.js kurulacak                 | Frontend     | ✅   |
| Proje klasör yapısı         | components / pages / services oluşturulacak | Frontend     | ✅   |
| Dosya yükleme ekranı        | txt / pdf yükleme UI yapılacak              | Frontend     | ✅   |
| API bağlantı altyapısı      | Backend endpoint çağrısı hazırlanacak       | Frontend     | ✅   |
| Hata mesajları              | Upload başarısızsa kullanıcıya gösterilecek | Frontend     | ✅   |
| Loading ekranı              | İşlem sırasında spinner gösterilecek        | Frontend     | ✅   |

---

# Contributor B

## Sorumluluk: LLM entegrasyonu ve ilk UML üretimi

| Görev                 | Açıklama                          | Sorumlu      | Durum |
| --------------------- | --------------------------------- | ------------ | ----- |
| Python ortam kurulumu | Virtual environment oluşturulacak | AI Developer | ❌   |
| LangChain kurulumu    | pip install langchain             | AI Developer | ❌   |
| LangGraph kurulumu    | Multi-agent sistem için           | AI Developer | ❌   |
| LLM API bağlantısı    | OpenAI / Claude / Llama           | AI Developer | ❌   |
| API anahtar yönetimi  | .env dosyasında saklanacak        | AI Developer | ❌   |
| Prompt tasarımı       | Ham metinden UML üretimi          | AI Developer | ❌   |
| İlk PlantUML üretimi  | Basit UML çıktısı alınacak        | AI Developer | ❌   |
| Prompt testleri       | Farklı metinlerle test yapılacak  | AI Developer | ❌   |
| Loglama sistemi       | Üretilen çıktılar kaydedilecek    | AI Developer | ❌   |

---

# Contributor C

## Sorumluluk: API geliştirme ve UML render sistemi

| Görev                      | Açıklama                    | Sorumlu | Durum |
| -------------------------- | --------------------------- | ------- | ----- |
| Backend framework kurulumu | FastAPI veya Flask          | Backend | ❌   |
| API endpoint oluşturma     | /generate-uml               | Backend | ❌   |
| Request validation         | Gelen veri kontrolü         | Backend | ❌   |
| LLM entegrasyonu           | API üzerinden model çağrısı | Backend | ❌   |
| PlantUML entegrasyonu      | UML kodu → görsel           | Backend | ❌   |
| PNG / SVG üretimi          | Diagram render              | Backend | ❌   |
| Hata yönetimi              | Exception handling          | Backend | ❌   |
| Unit test yazımı           | Endpoint testleri           | Test    | ❌   |
| API response formatı       | JSON standardı              | Backend | ❌   |

---

# Contributor D

## Sorumluluk: Test veri seti hazırlama ve UML/OCL standartlarını toplama

| Görev                  | Açıklama                        | Sorumlu         | Durum |
| ---------------------- | ------------------------------- | --------------- | ----- |
| PURE dataset indirme   | Resmi veri seti alınacak        | Data Specialist | ✅  |
| Veri temizleme         | Gereksiz veriler çıkarılacak    | Data Specialist | ✅  |
| Gereksinim metni seçme | UML testinde kullanılacak       | Data Specialist | ✅  |
| Veri formatlama        | txt / json formatına dönüştürme | Data Specialist | ✅  |
| Test veri klasörü      | data/test oluşturulacak         | Data Specialist | ❌  |
| OCL kuralları toplama  | UML doğrulama kuralları         | Data Specialist | ❌  |
| UML standart dokümanı  | UML specification               | Data Specialist | ❌ |
| Doküman depolama       | docs klasörüne koyma            | Data Specialist | ❌ |
| Version kontrol        | Veri seti versiyonlama          | Data Specialist | ❌ |

---

# 📦 Teknik Teslimatlar (Deliverables)

| Teslimat          | Açıklama             | Durum |
| ----------------- | -------------------- | ----- |
| Frontend arayüz   | Dosya yükleme ekranı | ✅   |
| Backend API       | UML üretim endpoint  | ❌   |
| AI üretim sistemi | PlantUML çıktısı     | ❌   |
| Render sistemi    | UML görsel üretimi   | ❌   |
| Test veri seti    | Temizlenmiş veri     | ✅   |
| Dokümantasyon     | UML ve OCL kuralları | ❌   |

---

# 📈 Haftalık Başarı Kriterleri

- [ ] Kullanıcı dosya yükleyebiliyor
- [ ] Backend API çalışıyor
- [ ] LLM bağlantısı aktif
- [ ] UML kodu üretiliyor
- [ ] UML görsel olarak render ediliyor
- [X] Test veri seti hazır

---

# 📝 Notlar

- Tüm geliştirmeler kendi branchimiz üzerinde yapılacaktır
- Merge işlemleri Pull Request ile yapılacaktır
- Kod review zorunludur
- Liste görevlerinde `- [x]` / `- [ ]` (gerekirse satıra `⏰` geç teslim, `❌` tamamlanmadı); tablolarda `⬜` / `✅` / `⏰` / `❌` (bkz. `checkpoint-kullanim-rehberi.md`)

---
