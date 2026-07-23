# Frontend Kurulum Rehberi

Bu belge, **UML Onarım Motoru** projesinin React + Vite tabanlı web arayüzünü yerelde ayağa kaldırmak ve geliştirmek için gereken adımları anlatır. Tüm komutlar `frontend` klasörü kökünde çalıştırılır.

---

## Gereksinimler

| Yazılım | Not |
|---------|-----|
| **Node.js** | LTS (ör. 20.x veya üzeri) önerilir |
| **npm** | Node ile birlikte gelir |

Tam işlev için backend API’nin erişilebilir olması gerekir. Geliştirmede genelde `http://localhost:8000` altında çalışan bir API kullanılır; adres `VITE_API_URL` ile ayarlanır.

---

## İlk kurulum

1. Depoda `frontend` dizinine girin:

   ```bash
   cd frontend
   ```

2. Bağımlılıkları yükleyin:

   ```bash
   npm install
   ```

3. Ortam dosyasını oluşturun. Repoda `.env.example` şablonu varsa kopyalayın; yoksa aşağıdaki bölümdeki örneği kullanın:

   ```bash
   cp .env.example .env
   ```

   Windows’ta `copy .env.example .env` kullanabilirsiniz.

---

## Ortam değişkenleri

Vite, yalnızca `VITE_` ile başlayan değişkenleri istemci koduna aktarır. `frontend` kökünde `.env` veya `.env.local` dosyası oluşturun.

| Değişken | Açıklama |
|----------|----------|
| `VITE_API_URL` | Backend API’nin kök adresi. Uygulama istekleri bu adresin **altına** eklenir (`/upload`, `/process/...` vb.). |

Örnek:

```env
VITE_API_URL=http://localhost:8000
```

`VITE_API_URL` tanımlı değilse kod içi varsayılan: `http://localhost:8000` (`src/services/api.js`).

`.env` değişikliğinden sonra geliştirme sunucusunu yeniden başlatın.

---

## Çalıştırma

| Amaç | Komut |
|------|--------|
| Geliştirme sunucusu (HMR) | `npm run dev` |
| Üretim derlemesi (`dist/`) | `npm run build` |
| `dist` çıktısını yerel önizleme | `npm run preview` |
| ESLint | `npm run lint` |

Geliştirme adresi genelde **http://localhost:5173** (Vite varsayılanı). Port doluysa Vite başka bir port önerebilir; terminal çıktısındaki URL’yi kullanın.

---

## Backend ile birlikte kullanım

1. Backend’i dokümantasyonuna göre başlatın.
2. Frontend `.env` içinde `VITE_API_URL` değerinin backend’in gerçek taban yolu ile uyumlu olduğundan emin olun (yol sonunda `/api` kullanımı proje ile uyumlu olmalı).
3. Tarayıcıda CORS hatası alırsanız ayarı backend tarafında düzeltmeniz gerekir; frontend yalnızca yapılandırılan adrese istek atar.

---

## API uçları (özet)

İstek tabanı: `{VITE_API_URL}` (ör. `http://localhost:8000`).

| Yöntem | Yol | Kullanım |
|--------|-----|----------|
| `POST` | `/upload` | Çok parçalı form: zorunlu alan `file` (SRS: `.txt` veya `.pdf`), isteğe bağlı `existing_uml` (mevcut UML: örn. `.xmi`, `.puml`, `.plantuml`) |
| `POST` | `/process/:fileId` | Yükleme yanıtındaki `fileId` ile işlem başlatma |
| `GET` | `/results/:jobId` | Serviste `getResults` ile tanımlı; akışta kullanımı backend sözleşmesine bağlı |

Backend’in `/upload` uç noktasında `existing_uml` alanını işlemesi gerekir; alan yoksa yalnızca SRS ile devam edilir. Gerçek JSON şemaları backend ile doğrulanmalıdır.

---

## Kaynak kod yapısı (özet)

```
frontend/
├── src/
│   ├── main.jsx, App.jsx
│   ├── components/     # Header, FileUpload, Alert, LoadingSpinner
│   ├── pages/          # HomePage
│   ├── services/       # api.js (Axios)
│   └── context/        # ThemeContext
├── public/
├── vite.config.js
├── package.json
└── .env.example
```

---

## Sık sorunlar

- **Ağ hatası / bağlanılamıyor:** Backend çalışıyor mu, `VITE_API_URL` doğru mu kontrol edin.
- **Değişken görünmüyor:** Değişken adı `VITE_` ile mi başlıyor, sunucu yeniden başlatıldı mı?
- **Yükleme reddedildi:** SRS için `.txt` / `.pdf` (zorunlu); isteğe bağlı mevcut UML için `.xmi`, `.uml`, `.puml`, `.plantuml` — her alan tek dosya, en fazla **10 MB** (`FileUpload.jsx`, `HomePage.jsx`).

---

## Sürüm notu

Bu rehber, `frontend` paketindeki betikler ve `src/services/api.js` ile uyumludur; bağımlılık veya API sözleşmesi değişince güncellenmelidir.
