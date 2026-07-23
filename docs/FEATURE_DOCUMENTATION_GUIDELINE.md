# FEATURE DOCUMENTATION GUIDELINE

## Amaç

Bu doküman, projeye eklenen her yeni özellik (feature), modül veya
sistem bileşeni için hazırlanacak dokümantasyon standardını tanımlar.

Amaç:

-   Her özelliğin kurulabilir olmasını sağlamak
-   Sistemin sürdürülebilirliğini artırmak
-   Yeni geliştiricilerin sistemi hızlı anlamasını sağlamak
-   Teknik değişikliklerin kayıt altına alınması

Kural:

Kod yazmak yeterli değildir.\
Kurulabilir ve anlaşılabilir hale getirmek zorunludur.

------------------------------------------------------------------------

## 1. Ne Zaman Dokümantasyon Yazılır?

Aşağıdaki durumlarda dokümantasyon zorunludur:

-   Yeni feature geliştirildiğinde
-   Yeni modül eklendiğinde
-   Yeni servis entegre edildiğinde
-   Yeni bağımlılık eklendiğinde
-   API endpoint değiştiğinde
-   Veritabanı yapısı değiştiğinde
-   Konfigürasyon değiştiğinde
-   Kurulum adımları değiştiğinde
-   Sistem davranışı değiştiğinde

Kural:

Her teknik değişiklik → Dokümantasyon gerektirir

------------------------------------------------------------------------

## 2. Dosya Konumu

Tüm feature dokümantasyonları aşağıdaki klasörde tutulur:

docs/features/

Örnek:

docs/features/login-system.md\
docs/features/file-upload.md\
docs/features/rag-module.md

------------------------------------------------------------------------

## 3. Dosya İsimlendirme Standardı

Format:

feature-name.md

Kurallar:

-   Küçük harf kullanılmalı
-   Boşluk yerine tire (-) kullanılmalı
-   Türkçe karakter kullanılmamalı
-   Açıklayıcı olmalı

Doğru:

user-authentication.md\
file-upload-system.md\
rag-integration.md

Yanlış:

Yeni Özellik.md\
test.md\
ozellik1.md

------------------------------------------------------------------------

## 4. Zorunlu Bölümler

Her feature dokümantasyonu aşağıdaki bölümleri içermelidir.

------------------------------------------------------------------------

# Feature Name

## Açıklama

Bu özellik ne yapar?

## Amaç

Bu özellik neden geliştirildi?

## Kurulum

Adım adım kurulum yazılmalıdır.

Örnek:

pip install requirements.txt

veya

npm install

------------------------------------------------------------------------

## Konfigürasyon

Gerekli ortam değişkenleri.

Örnek:

JWT_SECRET=secret\
DATABASE_URL=postgresql://user:pass@localhost/db

------------------------------------------------------------------------

## Kullanım

Bu özellik nasıl çalıştırılır?

Örnek:

npm run dev

veya

POST /api/login

------------------------------------------------------------------------

## Bağımlılıklar

Bu özellik için gerekli kütüphaneler:

-   library1
-   library2
-   library3

------------------------------------------------------------------------

## Dosya Yapısı

Bu özellik hangi dosyaları ekledi veya değiştirdi?

Örnek:

backend/\
auth/\
login.py

frontend/\
pages/\
Login.jsx

------------------------------------------------------------------------

## API (Varsa)

Endpoint:

POST /api/example

Request:

{ "example": "value" }

Response:

{ "status": "success" }

------------------------------------------------------------------------

## Veritabanı Değişiklikleri (Varsa)

Yeni tablo:

users

Alanlar:

-   id
-   email
-   password
-   created_at

------------------------------------------------------------------------

## Test

Bu özellik nasıl test edilir?

1.  Sunucuyu başlat
2.  Endpoint çağır
3.  Sonucu kontrol et

------------------------------------------------------------------------

## Hata Senaryoları

Bilinen hatalar:

-   Yanlış veri gönderildiğinde hata döner
-   Yetkisiz erişimde 401 döner

------------------------------------------------------------------------

## Geliştiren

İsim:\
Tarih:

------------------------------------------------------------------------

## Değişiklik Geçmişi

v1.0 --- İlk sürüm\
v1.1 --- Güncelleme

------------------------------------------------------------------------

## 5. Pull Request Kuralı

Yeni feature ekleyen kişi:

Şunları yapmak zorundadır:

-   Feature kodunu eklemek
-   Feature dokümantasyonunu yazmak
-   Pull Request açmak

Eksik dokümantasyon → PR reddedilir

------------------------------------------------------------------------

## 6. Kontrol Listesi

Feature ekledin mi?

Kontrol et:

\[ \] Dokümantasyon yazıldı\
\[ \] Kurulum adımları yazıldı\
\[ \] Kullanım açıklandı\
\[ \] Bağımlılıklar yazıldı\
\[ \] Test adımları yazıldı\
\[ \] PR açıldı

------------------------------------------------------------------------

## Son Kural

Kod yazıldıysa dokümantasyon yazılır.\
Dokümantasyon yoksa feature tamamlanmış sayılmaz.
