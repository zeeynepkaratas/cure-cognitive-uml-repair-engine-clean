# CURE Backend Manual Review Sample

Bu iç doküman, Backend doğrulama kapsamındaki `backend/src/ocl_engine/`
ve `backend/src/evaluators/` çıktılarının küçük bir elle doğrulama örneklemiyle
gözden geçirilmesi için hazırlanmıştır. Makale metnine eklenmemelidir; yalnızca
proje içi kontrol ve danışmanla paylaşılabilecek destek materyali olarak
kullanılmalıdır.

## Amaç

- `ocl_engine` tarafından üretilen ihlal/uyarı çıktılarının insan gözüyle
  makul olup olmadığını kontrol etmek.
- Bağımsız ground truth veri seti bulunmadığı durumda, küçük bir doğrulama
  örneklemiyle sınırlı fakat izlenebilir bir kalite notu üretmek.
- Onay sütunları doldurulduktan sonra makaleye yalnızca kısa bir metodolojik
  not eklemek; bu tabloyu makaleye koymamak.

## İnceleme Şablonu

| No | PlantUML girdisi / senaryo | Beklenen ihlal türü | Sistem çıktısı | Skor | Yazar içi onay | Not |
|---:|---|---|---|---:|---|---|
| 1 | `class UserManager {}\n@enduml` | Eksik başlangıç etiketi | Hata: `@startuml etiketi eksik` | %80.0 | Onaylandı | Beklenen hata doğru yakalanmış. Skorun %80 kalması makul; tek yapısal eksik var. |
| 2 | `@startuml\nclass UserManager {}` | Eksik bitiş etiketi | Hata: `@enduml etiketi eksik` | %80.0 | Onaylandı | Kapanış etiketi eksikliği açık ve sistem çıktısı beklenenle uyumlu. |
| 3 | `@startuml\n@enduml` | Boş diyagram | Hata: `Hic sinif tanimlanmamis` | %80.0 | Onaylandı | Boş diyagramı hata sayması doğru. Mesajın Türkçe karakter desteği ayrıca iyileştirilebilir. |
| 4 | `class UserManager {}` | Eksik başlangıç ve bitiş etiketi | Hata: `@startuml etiketi eksik`; `@enduml etiketi eksik` | %60.0 | Kısmen | İki ana eksik de bulunmuş. Skorun daha düşük verilmesi anlaşılır, ancak onarım sonrası davranış ayrıca test edilmeli. |
| 5 | `class userManager {}` | PascalCase ihlali | Uyarı: `Sinif isimlendirme kurali ihlali` | %95.0 | Onaylandı | İsimlendirme uyarısı yerinde. Bu durumun hata değil uyarı olarak kalması daha uygun görünüyor. |
| 6 | İki kez `class UserManager {}` | Tekrarlanan sınıf adı | Hata: `Tekrar eden sinif ismi`; uyarı: izole sınıf | %75.0 | Kısmen | Duplicate sınıf hatası doğru. İzole sınıf uyarısı bu örnekte ikincil/gürültülü olabilir. |
| 7 | İki ilişkisiz sınıf | İzole sınıf | Uyarı: `Izole sinif` | %95.0 | Onaylandı | Beklenen uyarı üretilmiş. Küçük diyagramlarda bunun her zaman problem sayılmayabileceği not edilmeli. |
| 8 | `Aaaa --> Bbbb` ve `Bbbb --> Aaaa` | Döngüsel bağımlılık | Uyarı: `Dongusel bagimlilik tespit edildi` | %95.0 | Onaylandı | Döngü tespiti doğru. Uyarı seviyesi bu basit örnek için yeterli. |
| 9 | 11 metotlu `HugeService` | God Class | Uyarı: `God Class: sinif cok fazla metot iceriyor (>10)` | %95.0 | Kısmen | Eşik bazlı tespit çalışıyor. Sadece metot sayısıyla karar verildiği için akademik metinde bu sınır açık belirtilmeli. |
| 10 | 21 sınıflı diyagram | Karmaşıklık | Uyarı: `Cok fazla sinif`; ayrıca izole sınıf uyarıları | %90.0 | Kısmen | Karmaşıklık uyarısı beklenenle uyumlu. İzole sınıf uyarıları çok sayıda gelirse rapor okunabilirliğini azaltabilir. |
| 11 | Eksik `@enduml`, `class badName {}`, `class OtherClass {}` | Karışık hata/uyarı | Hata: eksik bitiş etiketi; uyarı: PascalCase ve izole sınıf | %70.0 | Onaylandı | Birden fazla problemi birlikte yakalaması olumlu. Skor, hata ve uyarıların toplam etkisini kabaca yansıtıyor. |
| 12 | Duplicate sınıf + döngü | Karışık hata/uyarı | Hata: tekrar eden sınıf; uyarı: döngüsel bağımlılık | %75.0 | Onaylandı | Hem yapısal tekrar hem de ilişki döngüsü raporlanmış. Bu satır karma hata senaryosu için yeterli. |
| 13 | `UserManager --> DiagramService` içeren geçerli basit diyagram | İhlal yok | Hata/uyarı yok | %100.0 | Kısmen | Basit geçerli diyagramda temiz çıkması doğru. Yine de %100 ifadesi yalnızca bu küçük örnek için okunmalı, genel başarı gibi sunulmamalı. |

## Kullanım Notu

Bu tablo, bağımsız ve tam kapsamlı bir ground truth değil; yalnızca küçük bir
elle kontrol örneklemidir. `Onaylandı` etiketi, ilgili satırdaki beklenen
ihlal/uyarı için sistem çıktısının makul bulunduğunu belirtir. `Kısmen`
etiketi ise çıktının ana beklentiyi karşıladığı, fakat skor, ek uyarı veya
yorumlama açısından sınırlılık taşıdığı durumlarda kullanılmıştır.

Makalede bu tabloya dayanılacaksa, sonuçların yalnızca sınırlı bir manuel
kontrol örneklemi olduğu ve bağımsız uzman doğrulaması yerine geçmediği açıkça
belirtilmelidir.
