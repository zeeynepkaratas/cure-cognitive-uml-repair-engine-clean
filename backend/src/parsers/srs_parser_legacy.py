import re
from typing import Optional

# İlişki kalıpları — SRS belgelerinde yaygın fiiller
RELATIONSHIP_PATTERNS = [
    (r'\b(\w+)\s+(?:uses?|utilizes?)\s+(?:the\s+)?(\w+)', 'uses'),
    (r'\b(\w+)\s+(?:extends?|inherits?)\s+(?:the\s+)?(\w+)', 'extends'),
    (r'\b(\w+)\s+(?:implements?)\s+(?:the\s+)?(\w+)', 'implements'),
    (r'\b(\w+)\s+(?:contains?|has)\s+(?:a|an|one|many|the)?\s*(\w+)', 'has'),
    (r'\b(\w+)\s+(?:manages?|handles?)\s+(?:the\s+)?(\w+)', 'manages'),
    (r'\b(\w+)\s+(?:creates?|generates?)\s+(?:the\s+)?(\w+)', 'creates'),
    (r'\b(\w+)\s+(?:communicates?\s+with|connects?\s+to)\s+(?:the\s+)?(\w+)', 'connects'),
    (r'\b(\w+)\s+(?:sends?|notifies?)\s+(?:\w+\s+)?(?:to\s+)?(?:the\s+)?(\w+)', 'sends'),
    (r'\b(\w+)\s+(?:stores?|retrieves?)\s+(?:\w+\s+)*(?:from\s+)?(?:the\s+)?(\w+)', 'stores'),
    (r'\b(\w+)\s+(?:depends?\s+on|relies?\s+on)\s+(?:the\s+)?(\w+)', 'depends'),
    (r'\b(\w+)\s+(?:calls?|invokes?)\s+(?:the\s+)?(\w+)', 'uses'),
    (r'\b(\w+)\s+(?:accesses?)\s+(?:the\s+)?(\w+)', 'uses'),
    (r'\b(\w+)\s+(?:interacts?\s+with)\s+(?:the\s+)?(\w+)', 'connects'),
    (r'\b(\w+)\s+(?:delegates?\s+to)\s+(?:the\s+)?(\w+)', 'uses'),
]

# Kesinlikle sınıf olmayan kelimeler
STOP_WORDS = {
    # Zamirler ve belirteçler
    'the','a','an','is','are','was','were','be','been','being',
    'have','has','had','do','does','did','will','would','could',
    'should','may','might','shall','can','need','must','ought',
    'this','that','these','those','it','its','they','them','their',
    'when','where','which','who','how','what','all','each','every',
    # Bağlaçlar ve edatlar
    'and','or','but','not','with','from','into','onto','upon',
    'after','before','during','while','through','about','over',
    # Genel yazılım terimleri (sınıf adı olamaz)
    'system','user','data','information','process','function',
    'feature','requirement','functionality','operation','action',
    'input','output','result','value','type','list','item','set',
    # Kısaltmalar (sınıf değil)
    'api','rest','json','xml','html','css','sql','url',
    'http','https','pdf','csv','srs','ocl','llm','ai','ui','ux',
    'sms','mms','ftp','tcp','ip','id','ui','db',
    # Modal fiiller ve kip belirteçleri
    'shall','must','should','will','can','may','need',
    # Yaygın İngilizce isimler (sınıf değil)
    'email','password','token','role','record','session',
    'request','response','message','error','status','code',
    'name','date','time','number','version','level','mode',
    'active','current','new','old','base','core','main',
}

# Teknik sınıf son ekleri — bunları içeren kelimeler büyük ihtimalle sınıftır
CLASS_SUFFIXES = (
    'Service','Manager','Controller','Repository','Handler',
    'Engine','Validator','Parser','Generator','Processor',
    'Factory','Builder','Monitor','Analyzer','Evaluator',
    'Executor','Scheduler','Adapter','Provider','Client',
    'Server','Gateway','Proxy','Registry','Store','Cache',
    'Dispatcher','Observer','Listener','Notifier','Sender',
)

def is_valid_class(word: str) -> bool:
    """Bir kelimenin sınıf adı olup olmadığını kontrol eder."""
    if word.lower() in STOP_WORDS:
        return False
    if len(word) < 4:
        return False
    # Tamamen büyük harf (kısaltma) — sınıf değil
    if word.isupper() and len(word) <= 4:
        return False
    # PascalCase veya bilinen suffix içermeli
    if not re.match(r'^[A-Z][a-zA-Z0-9]{2,}$', word):
        return False
    return True

def extract_classes(text: str) -> list:
    """
    Metinden sınıf adaylarını çıkarır.
    Öncelik sırası: bilinen suffix > CamelCase > domain noun
    """
    candidates = {}  # word -> score

    # 1. Yüksek güven: bilinen teknik suffix içerenler
    for suffix in CLASS_SUFFIXES:
        pattern = rf'\b([A-Z][a-zA-Z0-9]*{suffix})\b'
        for match in re.finditer(pattern, text):
            word = match.group(1)
            if is_valid_class(word):
                candidates[word] = candidates.get(word, 0) + 3  # yüksek skor

    # 2. Orta güven: CamelCase (birden fazla büyük harf içeren)
    for match in re.finditer(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b', text):
        word = match.group(1)
        if is_valid_class(word):
            candidates[word] = candidates.get(word, 0) + 2

    # 3. Düşük güven: büyük harfle başlayan tekil kelimeler (3+ tekrar edenler)
    singles = re.findall(r'\b([A-Z][a-zA-Z]{3,})\b', text)
    freq = {}
    for w in singles:
        freq[w] = freq.get(w, 0) + 1
    for word, count in freq.items():
        if count >= 2 and is_valid_class(word) and word not in candidates:
            candidates[word] = count

    # Skora göre sırala, max 12 sınıf
    sorted_classes = sorted(candidates.items(), key=lambda x: -x[1])
    return [w for w, _ in sorted_classes[:12]]


def extract_relationships(text: str, classes: list) -> list:
    """
    Metinden sınıflar arası ilişkileri çıkarır.
    Büyük/küçük harf duyarsız eşleştirme yapar.
    """
    relationships = []
    seen = set()
    class_lower_map = {c.lower(): c for c in classes}

    for pattern, rel_type in RELATIONSHIP_PATTERNS:
        for src_raw, tgt_raw in re.findall(pattern, text, re.IGNORECASE):
            src_key = src_raw.strip().lower()
            tgt_key = tgt_raw.strip().lower()

            # Her iki taraf da bilinen sınıflar içinde olmalı
            src = class_lower_map.get(src_key)
            tgt = class_lower_map.get(tgt_key)

            if not src or not tgt or src == tgt:
                continue

            key = (src, tgt)
            if key in seen:
                continue
            seen.add(key)

            relationships.append({
                "source": src,
                "target": tgt,
                "type": rel_type
            })

    return relationships


def generate_plantuml(classes: list, relationships: list) -> str:
    """Sınıf ve ilişkilerden PlantUML kodu üretir."""
    lines = ["@startuml", "skinparam classAttributeIconSize 0", ""]

    for cls in classes:
        lines.append(f"class {cls} {{")
        lines.append("}")
        lines.append("")

    if relationships:
        lines.append("' Iliskiler")
        for rel in relationships:
            if rel["type"] in ("extends", "implements"):
                lines.append(f'{rel["source"]} --|> {rel["target"]}')
            elif rel["type"] == "has":
                lines.append(f'{rel["source"]} *-- {rel["target"]}')
            else:
                lines.append(f'{rel["source"]} --> {rel["target"]}')

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


def srs_to_plantuml(srs_metni: str) -> dict:
    """
    Ana fonksiyon: SRS metnini PlantUML diyagramına çevirir.
    """
    if not srs_metni or len(srs_metni.strip()) < 10:
        return {
            "plantuml_kodu": "@startuml\n@enduml",
            "bulunan_siniflar": [],
            "iliskiler": [],
            "sinif_sayisi": 0,
            "hata": "Metin çok kısa veya boş"
        }

    try:
        classes = extract_classes(srs_metni)
        relationships = extract_relationships(srs_metni, classes)
        plantuml = generate_plantuml(classes, relationships)

        return {
            "plantuml_kodu": plantuml,
            "bulunan_siniflar": classes,
            "iliskiler": relationships,
            "sinif_sayisi": len(classes),
            "hata": None
        }
    except Exception as e:
        return {
            "plantuml_kodu": "@startuml\n@enduml",
            "bulunan_siniflar": [],
            "iliskiler": [],
            "sinif_sayisi": 0,
            "hata": str(e)
        }


if __name__ == "__main__":
    test_srs = """
    The AuthenticationService handles user login, logout, and password reset.
    The UserRepository stores and retrieves user records from the database.
    The SessionManager manages active user sessions and token expiration.
    The NotificationService sends email and SMS notifications to users.
    The AuthenticationService uses the UserRepository to verify credentials.
    The AuthenticationService communicates with the SessionManager to create sessions.
    The SessionManager sends token data to the NotificationService.
    The AdminController manages system configuration and user roles.
    The AdminController extends the BaseController with admin-specific permissions.
    """
    result = srs_to_plantuml(test_srs)
    print("Sınıflar:", result["bulunan_siniflar"])
    print("İlişkiler:", [(r["source"], r["type"], r["target"]) for r in result["iliskiler"]])
    print()
    print(result["plantuml_kodu"])
