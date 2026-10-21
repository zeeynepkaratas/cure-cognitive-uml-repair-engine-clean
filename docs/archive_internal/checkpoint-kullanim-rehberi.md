# 📘 Checkpoint Dokümanı Kullanım Rehberi

Bu rehber, proje ekip üyelerinin **checkpoint (haftalık görev listesi)
dokümanını nasıl kullanacağını** açık ve standart bir şekilde anlatmak
için hazırlanmıştır.


------------------------------------------------------------------------

# 🎯 Amaç

Checkpoint dokümanının amacı:

-   Görevlerin net şekilde tanımlanması
-   Sorumluların belirlenmesi
-   İlerlemenin takip edilmesi
-   Haftalık kontrol yapılması
-   Sprint hedeflerinin doğrulanması

------------------------------------------------------------------------

# 📂 Doküman Yapısı

Checkpoint dosyası genellikle şu bölümlerden oluşur:

-   Genel Hedefler
-   Görev Dağılımı
-   Teknik Teslimatlar
-   Başarı Kriterleri
-   Durum İşaretleme (Checkbox)

Örnek (liste satırları):

-   [ ] Görev tamamlanmadı
-   [x] Görev tamamlandı

Tablo **Durum** sütunu için: `⬜` / `✅` / `⏰` / `❌` (anlamları aşağıda). Ayrıntı için *Checkbox (İşaretleme)* bölümüne bakın.

------------------------------------------------------------------------

# 🧑‍💻 Kim Ne Yapacak?

Her ekip üyesi:

1.  Kendi sorumluluk alanını bulur
2.  Görev listesini inceler
3.  Görevi tamamladığında işaretler
4.  Gerekirse not ekler
5.  Pull Request açar

------------------------------------------------------------------------

# ✅ Checkbox (İşaretleme) Kullanımı

## Liste satırları (madde işaretli görevler)

Görev tamamlandığında **yalnızca küçük harf `x`** kullanın. Büyük `X` birçok Markdown görüntüleyicide işaretli kutu olarak **görünmez**; metin gibi kalır.

Önce:

-   [ ] Backend API oluşturma

Sonra:

-   [x] Backend API oluşturma

**Yapılmaması gerekenler:**

-   `[X]` (büyük X) — çoğu ortamda yanlış görünür
-   Görev bitmeden `[x]` koymak

**Liste biçimi:** Madde işareti olarak `-` (tire) kullanmanız önerilir; `*` ile de yazılabilir, ancak `- [x]` / `- [ ]` kalıbı en yaygın okunur biçimdir.

## Tablolardaki “Durum” sütunu

GitHub vb. ortamlarda **tablo hücresinin içinde** yazılan `[ ]` / `[x]` çoğu zaman **tıklanabilir checkbox olarak render edilmez**; düz metin gibi görünür. Bu yüzden checkpoint tablolarında durum için aşağıdaki **standart işaretler** ve **açıklamalar** kullanılır.

### İşaretlerin açıklaması

-   **`⬜` (Bekliyor)** — Görev tanımlı, üzerinde çalışılıyor veya henüz başlanmadı; sprint bitiş tarihine kadar sonuç net değil. Tamamlanınca bu hücre `✅`, `⏰` veya `❌` ile değiştirilir.

-   **`✅` (Süresi içinde tamamlandı)** — İş **Görev Bitiş Tarihi dahil, o tarihe kadar** teslim edildi. Yani son teslim günü **dahil** tamamlanan işler bu işareti alır. **Yanlış kullanım:** Bitiş tarihinden *sonra* biten bir işi `✅` göstermek; bu durumda mutlaka `⏰` kullanılmalıdır.

-   **`⏰` (Geç teslim — zaman / süre aşımı)** — Görev **fiilen tamamlandı** ancak teslim, ilgili checkpoint’in **Görev Bitiş Tarihi’nden sonra** gerçekleşti. Bu, “zamanında bitmedi ama yapıldı” durumunun tek doğru işaretidir.

-   **`❌` (Tamamlanmadı / yapılmadı)** — Bitiş tarihi geldiğinde veya sprint kapanırken görev **hiç tamamlanmadı** veya teslim edilemedi. `⏰` ile karıştırılmamalıdır: `⏰` iş bitmiş demektir; `❌` iş bitmemiş demektir.

**Zorunlu kural (süre bittikten sonra tamamlanan iş):** Checkpoint’te yazılı **Görev Bitiş Tarihi** geçtikten sonra tamamlanan her görevde, tabloda ve listede **`✅` kullanılmaz**; teslim zamanı geçmiş olduğu için **`⏰` konulması zorunludur.** Süre içinde bitmiş gibi göstermek için `✅` yazmak doğru değildir. Liste satırında da aynı mantık geçerli: geç biten iş `- [x] … ⏰` veya açık `(geç teslim)` notu ile işaretlenir.

Özet tablo:

| Anlamı | İşaret (önerilen) | Alternatif metin |
| ------ | ----------------- | ---------------- |
| Henüz bitmedi / bekliyor | `⬜` | `Bekliyor` |
| Süre içinde tamamlandı (bitiş tarihine kadar teslim) | `✅` | `Tamamlandı` |
| Süre bittikten sonra tamamlandı (geç teslim) | `⏰` | `Geç teslim` |
| Süre sonunda tamamlanmadı | `❌` | `Tamamlanmadı` veya `Yapılmadı` |

Emoji ile metin **aynı satırda karıştırılmaz**: ya dörtlü emoji seti ya da dörtlü metin seti kullanın. Güncellerken yalnızca ilgili hücreyi değiştirmeniz yeterlidir.

## Liste satırlarında “geç teslim” ve “tamamlanmadı”

Standart checkbox yalnızca **boş / tamam** iki durumu bilir. Üçüncü ve dördüncü durumları şöyle gösterebilirsiniz:

-   **Süresi içinde bitti:** `- [x] Görev adı` (bitiş tarihine kadar teslim; yukarıdaki `✅` ile aynı anlam)

-   **Süre bittikten sonra tamamlandı (zorunlu `⏰`):** `- [x] Görev adı ⏰` veya satır sonuna `(geç teslim)` yazın. Bitiş tarihinden sonra biten işte **`⏰` veya eşdeğer not olmadan** sadece `[x]` bırakmak yeterli sayılmaz; zaman aşımı mutlaka görünür olmalıdır.

-   **Tamamlanmadı:** `- [ ] Görev adı` bırakıp not düşün veya checkbox yerine `- ❌ Görev adı — tamamlanmadı` satırı kullanın (checkpoint’te tutarlı olun)

Kural:

Her görev tamamlanmadan “tamamlandı” (`✅` / `[x]`) işareti konmamalıdır.

------------------------------------------------------------------------

# ⏰ Görev bitiş tarihi ve commit kabulü

Her checkpoint’te **Görev Bitiş Tarihi** alanı tanımlıdır. Bu tarih, o haftanın görevlerinin kapanışını belirtir.

-   **Bitiş tarihinden sonra** ilgili haftanın kapsamı için yapılan **commit’ler kabul edilmez** (PR merge edilmez veya değerlendirmeye alınmaz; ekip içi kuralınıza göre netleştirin). Bu, **kod teslim / repo** politikasıdır. **Checkpoint dosyasındaki** `⏰` veya liste notu, işin fiilen geç bittiğini göstermek içindir; yasaklanan commit’ler merge edilmediği sürece tabloda yine **`❌`** kalabilir — ikisi çelişmez, farklı katmanları anlatır.
-   Bitiş tarihine kadar **hiç tamamlanmamış** görevler **yapılmadı** kabul edilir; tabloda **`❌` (Tamamlanmadı)** veya uygunsa **`⬜` (Bekliyor)** kullanılır.

**Süre dolduktan sonra iş tamamlanmışsa:** Teslim, bitiş tarihinden sonra gerçekleşmiş olsa bile görev teknik olarak yapılmış olabilir. Bu durumda checkpoint’te **`✅` değil, mutlaka `⏰` (Geç teslim)** kullanılır. Zamanında bitmiş gibi raporlamak için `✅` yazılmaz; süre aşımı `⏰` ile açıkça belirtilir (ayrıntı: yukarıdaki *İşaretlerin açıklaması* ve *Zorunlu kural*).

### Durum güncellemesi için son pencere (bir sonraki checkpoint)

Her checkpoint dosyasındaki **durum işaretleri** (`⬜` / `✅` / `⏰` / `❌`), **bir sonraki checkpoint’in Görev Bitiş Tarihi dahil, o tarihe kadar** güncellenebilir. Bu süre içinde geç teslim (`⏰`) veya son düzeltmeler yansıtılabilir.

**Bir sonraki checkpoint’in bitiş tarihinden sonra:** O haftaya ait görevler daha sonra fiilen tamamlanmış olsa bile **bu checkpoint dosyasında durum bilgisi güncellenmez**; ilgili haftanın kaydı **o tarih itibarıyla kapanmış** kabul edilir. İleriye dönük iş, yeni haftanın checkpoint’inde takip edilir.

**Son checkpoint (haftası):** İzleyen checkpoint dokümanı yoksa, durum güncellemesi için son tarih **Scrum Master (veya ekip)** ile netleştirilir (ör. proje teslimi veya son sprint tarihi).

Bu kural seti, checkpoint’in sprint takibi için güvenilir tek kaynak olmasını sağlar.

------------------------------------------------------------------------

# 🔄 Güncelleme Kuralları

Checkpoint dokümanı:

-   **Görev tabloları ve listelerdeki durum işaretleri** (`⬜` / `✅` / `⏰` / `❌`), izleyen checkpoint’in **Görev Bitiş Tarihi**ne kadar güncellenebilir; o tarihten sonra o dosyada bu işaretler değiştirilmez (üstteki **`Durum:`** renk satırı da bu dosya kapsamındadır; bkz. *Durum güncellemesi için son pencere*).
-   Açık pencerede günlük güncelleme beklenir
-   Sprint sonunda kontrol edilir
-   Scrum Master tarafından doğrulanır

------------------------------------------------------------------------

# 🧭 Günlük Kullanım Adımları

Her gün:

1.  Repo açılır
2.  Checkpoint dosyası açılır
3.  Kendi görevlerin kontrol edilir
4.  Tamamlanan görev işaretlenir
5.  Commit yapılır

------------------------------------------------------------------------

# 🪜 Örnek Günlük Workflow

1.  Görev seç
2.  Görevi yap
3.  Test et
4.  Commit yap
5.  Pull Request aç
6.  Görevi işaretle

------------------------------------------------------------------------

# ⚠️ Önemli Kurallar

-   Her görev branch üzerinden yapılır
-   Doğrudan main branch'e commit atılmaz
-   Pull Request zorunludur
-   Kod review yapılmadan merge edilmez
-   Görev tamamlanmadan tamamlandı işareti konmaz (liste: `[x]`; tablo: `✅` / `⏰` / `⬜` / `❌` — anlamları *İşaretlerin açıklaması* bölümünde)
-   **Görev bitiş tarihinden sonra** o haftaya ait iş için commit kabul edilmez; tamamlanmayanlar **yapılmadı** sayılır (`❌`)
-   **Bitiş tarihinden sonra** tamamlanan işlerde **`⏰` kullanımı zorunludur**; `✅` ile “zamanında” gösterilemez
-   **Bir sonraki checkpoint bitene kadar** o hafta dosyasında görev işaretleri ve üst **Durum:** güncellenebilir; **ondan sonra** görevler yapılmış olsa bile **bu dosyada güncellenmez**

------------------------------------------------------------------------

# 📅 Haftalık Kontrol (Sprint Review)

Hafta sonunda:

Kontrol edilir:

-   Hangi görevler tamamlandı
-   Hangi görevler eksik
-   Hangi görevler gecikti
-   Sistem çalışıyor mu

------------------------------------------------------------------------

# 📊 Durum satırı ve renkler

Checkpoint dosyasının üstündeki **`Durum:`** satırı, o haftanın **genel özetini** verir; görev tablolarındaki işaretler (`⬜`, `✅`, `⏰`, `❌`) ile aynı şey değildir — satır satır kanıt tabloda kalır, renkli satır ise okuyana kısa yönlendirme yapar.

**Ne yazılır:** Renk + kısa başlık + *parantez veya tire ile ufak bilgilendirme* (eksik var mı, tam mı kapandı, geç mi bitti). Uzun cümle yerine birkaç kelime yeterlidir.

**Süre / güncelleme:** Burada anlatılan “ne zaman bitti” veya “nasıl kapandı” yalnızca bu **özet satırının** ifadesidir. **Güncelleme penceresi**, **geç teslim (`⏰`)** ayrıntıları ve **bir sonraki checkpoint’e kadar güncelleme** kuralları yukarıdaki ilgili başlıklarda tanımlıdır.

### Renk — ana durumlar

| Renk | Özet başlık | Ufak bilgilendirme (örnekler) |
| ---- | ----------- | ------------------------------ |
| 🔴 | Başlanmadı / Henüz yok | `(henüz iş yok)`, `(planlama aşaması)` |
| 🟡 | Devam ediyor | `(kısmi ilerleme)`, `(eksikler var)`, `(risk yok / risk var)` |
| 🟠 | Risk / Gecikme | `(süre dar)`, `(geç teslim bekleniyor)`, `(bazı görevler ⏰)` |
| 🟢 | Tamamlandı | Aşağıdaki *Tamamlandı* alt türlerine bakın |


### “Tamamlandı” (🟢) — alt bilgilendirmeler

Hafta **kapandı** sayıldığında 🟢 kullanılır; okuyanın anlaması için parantezde **nasıl** tamamlandığı kısaca yazılır:

| Alt anlam | Durum satırına örnek |
| --------- | -------------------- |
| Tam — süresi içinde, kritik eksik yok | `Durum: 🟢 Tamamlandı (tam, süresi içinde)` |
| Tam — küçük/opsiyonel işler kaldı | `Durum: 🟢 Tamamlandı (tam; düşük öncelik işler sürebilir)` |
| Eksiklerle kapatıldı | `Durum: 🟢 Tamamlandı (eksiklerle; bazı görevler ❌/⬜)` |
| Geç tamamlandı | `Durum: 🟢 Tamamlandı (geç; ⏰ ile kapatıldı)` veya `(geç teslimlerle)` |

**Not:** “Eksiklerle” veya “geç” ifadesi, üst satırda özetlenir; hangi görevin `⏰` veya `❌` olduğu yine görev listesinde görülür.


------------------------------------------------------------------------

# 🧾 Commit Mesajı Standartı

Örnek:

feat: upload endpoint eklendi

fix: api hata yönetimi düzeltildi

docs: checkpoint güncellendi

------------------------------------------------------------------------

# 🧠 En İyi Kullanım Tavsiyeleri

-   Her görev küçük parçalara bölünmeli
-   Güncelleme penceresi açıkken mümkün olduğunca sık güncellenmeli
-   Sadece sorumlu kişi işaretlemeli
-   Scrum Master haftalık kontrol etmeli
-   Repo'da tek kaynak olarak kullanılmalı

------------------------------------------------------------------------

# 🎯 Kısa Özet

Checkpoint dokümanı:

-   Görev listesidir
-   İlerleme takip aracıdır
-   Sprint kontrol aracıdır
-   Ekip koordinasyon aracıdır
-   **Bir sonraki chechkpoint'in görev bitiş tarihinden sonra** ilgili haftaya ait commit kabul edilmez; süre sonunda hiç bitmeyen görevler **yapılmadı** (`❌`) sayılır.
-   İşaretleme: dört işaretin anlamı *İşaretlerin açıklaması* bölümündedir; **süre bittikten sonra tamamlanan** her işte tabloda ve listede **`⏰` zorunludur**, `✅` yanlıştır.
-   **Bir sonraki checkpoint’in bitişine kadar** geçmiş haftanın **görev durum işaretleri** ve üst **Durum:** özeti güncellenebilir; **o tarihten sonra** o hafta dosyasında **bunlar değiştirilmez** (iş kodda kalsa bile).
-   Üstteki **`Durum:`** satırı renk + kısa parantezli bilgilendirme ile haftayı özetler; ayrıntı *Durum satırı ve renkler* bölümündedir.
