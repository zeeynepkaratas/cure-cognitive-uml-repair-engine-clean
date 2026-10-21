# 📘 Git Commit Atma Rehberi (Detaylı)

Bu doküman, ekip üyelerinin **doğru ve standart şekilde commit
atmasını** sağlamak için hazırlanmıştır.

------------------------------------------------------------------------

# 🎯 Commit Nedir?

Commit:

Kodda yaptığın değişiklikleri **versiyon kontrol sistemine kaydetme
işlemidir**.

Yani:

Bir işi bitirdin → commit atarsın\
Bir hatayı düzelttin → commit atarsın\
Yeni özellik ekledin → commit atarsın

------------------------------------------------------------------------

# 🧠 Temel Mantık

Workflow:

Kod yaz → Stage → Commit → Push → Pull Request

------------------------------------------------------------------------

# 📌 Commit Atma Adımları (Standart)

## 1. Değişiklik Yap

Örnek:

-   Yeni API yazdın
-   UI tasarladın
-   Bug düzelttin

------------------------------------------------------------------------

## 2. Değişiklikleri Gör

Komut:

git status

Bu komut:

Hangi dosyalar değişmiş gösterir.

------------------------------------------------------------------------

## 3. Dosyaları Stage Et

Tek dosya:

git add app.py

Tüm dosyalar:

git add .

------------------------------------------------------------------------

## 4. Commit At

Komut:

git commit -m "mesaj"

Örnek:

git commit -m "feat: upload endpoint eklendi"

------------------------------------------------------------------------

## 5. Remote'a Gönder (Push)

git push

------------------------------------------------------------------------

# 🪜 Tam Workflow Örneği

git checkout -b feature/upload-api

git add .

git commit -m "feat: upload endpoint eklendi"

git push origin feature/upload-api

------------------------------------------------------------------------

# 🧾 Commit Mesajı Standartı (ÇOK ÖNEMLİ)

Format:

type: kısa açıklama

------------------------------------------------------------------------

# Commit Türleri

feat\
Yeni özellik

fix\
Hata düzeltme

docs\
Dokümantasyon değişikliği

refactor\
Kod düzenleme

test\
Test ekleme

style\
Format düzenleme

chore\
Genel bakım işleri

------------------------------------------------------------------------

# Örnek Commit Mesajları

feat: login ekranı eklendi

fix: null pointer hatası düzeltildi

docs: README güncellendi

refactor: service yapısı düzenlendi

test: api unit test eklendi

------------------------------------------------------------------------

# ❌ Yanlış Commit Mesajları

update

fix bug

deneme

123

------------------------------------------------------------------------

# ✔️ Doğru Commit Mesajı Özellikleri

-   Kısa
-   Açık
-   Ne yaptığını anlatır
-   İngilizce yazılır
-   Küçük harf ile başlar

------------------------------------------------------------------------

# 📦 Ne Zaman Commit Atılır?

Şu durumlarda:

-   Bir görev tamamlandığında
-   Bir bug düzeltildiğinde
-   Bir feature eklendiğinde
-   Bir test yazıldığında
-   Bir refactor yapıldığında

------------------------------------------------------------------------

# 🚫 Ne Zaman Commit Atılmaz?

Şu durumlarda:

-   Kod çalışmıyorsa
-   Hata varsa
-   Test edilmemişse
-   Yarım iş varsa

------------------------------------------------------------------------

# 📅 Günlük Commit Kuralı

Minimum:

Günde 1 commit

İdeal:

Her görev sonrası commit

------------------------------------------------------------------------

# 🧑‍💻 Branch Üzerinde Commit Atma

ÖNEMLİ:

Main branch'e commit atılmaz.

------------------------------------------------------------------------

Workflow:

git checkout develop

git pull

git checkout -b feature/login

Kod yaz

git add .

git commit -m "feat: login sistemi eklendi"

git push origin feature/login

------------------------------------------------------------------------

# 🔄 Commit Düzeltme

Son commit mesajını değiştirme:

git commit --amend

------------------------------------------------------------------------

# Commit Geri Alma

Son commit sil:

git reset --soft HEAD\~1


------------------------------------------------------------------------

# 🎯 Kısa Özet

Commit:

Kod değişikliğini kaydetmektir.

Standart:

git add .

git commit -m "feat: açıklama"

git push
