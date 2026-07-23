# 🌿 Branch Kullanım Rehberi

Bu doküman, proje içerisinde **branch (dal) kullanım standardını** ve **Pull Request (PR) sürecini** açıklamak amacıyla hazırlanmıştır. Tüm ekip üyeleri bu kurallara uymakla yükümlüdür.

---

## 🎯 Amaç

- Kod karışıklığını önlemek
- Her geliştiricinin izole şekilde çalışmasını sağlamak
- Kod kalitesini kontrol etmek
- Yayına alınacak kodun onay sürecinden geçmesini sağlamak

---

## 🧩 Branch Yapısı

Projede her geliştiriciye özel bir branch oluşturulmuştur.

**Ana branch:**

```
main
```

**Geliştirici branchleri:**

```
contributor-a
contributor-c
contributor-b
contributor-d
```

Her geliştirici **sadece kendi branch'inde** geliştirme yapar.

---

## 🔄 Çalışma Akışı (Workflow)

1. Kendi branch'ine geç
2. Değişiklikleri yap
3. Commit at
4. Remote'a push et
5. Pull Request (PR) aç
6. Onay bekle
7. Onaylandıktan sonra main branch'e merge edilir

Akış şeması mantığı:

```
Kendi Branch → PR Aç → Onay → Main'e Merge → Yayın
```

---

## 🧑‍💻 Geliştirici Adımları

### 1. Projeyi çek

```bash
git clone <repo-url>
cd <proje-adi>
```

### 2. Kendi branch'ine geç

```bash
git checkout feature-<isim>
```

Örnek:

```bash
git checkout feature-contributor-c
```

---

### 3. Değişiklik yap ve commit at

```bash
git add .
git commit -m "Yeni özellik eklendi"
```

---

### 4. Branch'i push et

```bash
git push origin feature-<isim>
```

---

### 5. Pull Request (PR) Aç

GitHub üzerinden:

1. Repository sayfasına git
2. **Compare & pull request** butonuna tıkla
3. Açıklama yaz
4. PR oluştur

---

## 🔒 Onay Süreci

Tüm Pull Request'ler proje sorumlusu tarafından incelenir.

Kurallar:

- PR onaylanmadan **main branch'e merge edilmez**
- Hatalı kod varsa geri gönderilir
- Gerekirse düzeltme istenir
- Sadece onaylanan kod yayına alınır

Süreç:

```
Developer → PR → Review → Onay → Merge → Yayın
```

---

## 📌 Branch İsimlendirme Kuralları

Standart format:

```
isimsoyisim
```

---

## ❗ Önemli Kurallar

- Kimse **main branch'e direkt push yapamaz**
- Her değişiklik PR üzerinden gelir
- Her geliştirici sadece kendi branch'inde çalışır
- Commit mesajları açıklayıcı olmalıdır
- Merge işlemi sadece proje sorumlusu tarafından yapılır

---

## 🧪 Örnek Senaryo

Bir katkıcı yeni bir özellik geliştirdi:

1. `contributor-c` branch'inde çalıştı
2. Commit attı
3. Push etti
4. PR açtı
5. Proje sorumlusu kodu inceledi
6. Onayladı
7. Kod main branch'e merge edildi
8. Sistem yayına alındı

---

## Versiyon

**v1.0 — Branch Kullanım ve PR Süreci Rehberi**
