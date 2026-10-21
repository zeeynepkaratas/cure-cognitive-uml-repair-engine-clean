import re
from typing import Optional

try:
    from utils.plantuml_parser import parse_classes, parse_relationships
except ModuleNotFoundError:  # package import path: src.evaluators.semantic_eval
    from src.utils.plantuml_parser import parse_classes, parse_relationships

# Sınıf adı olmayan genel kelimeler
STOP_WORDS = {
    'The','This','These','That','When','Where','Which','Each',
    'All','Any','Some','Both','For','And','But','Or','Not',
    'With','From','Into','Upon','After','Before','During',
    'the','this','these','that','when','where','which','each',
    'all','any','some','both','for','and','but','or','not',
    'with','from','into','upon','after','before','during',
    'System','User','Data','Information','Process','Function',
    'system','user','data','information','process','function',
    'Email','Password','Token','Role','Record','Session',
    'email','password','token','role','record','session',
    'Request','Response','Message','Error','Status','Code',
    'request','response','message','error','status','code',
    'SMS','MMS','API','URL','HTTP','PDF','CSV','SRS','OCL',
    'Active','Current','New','Old','Base','Core','Main',
    'active','current','new','old','base','core','main',
    'Database','Server','Client','Interface',
}

CLASS_SUFFIXES = (
    'Service','Manager','Controller','Repository','Handler',
    'Engine','Validator','Parser','Generator','Processor',
    'Factory','Builder','Monitor','Analyzer','Evaluator',
    'Executor','Scheduler','Adapter','Provider','Gateway',
    'Proxy','Registry','Store','Cache','Dispatcher',
    'Observer','Listener','Notifier','Sender',
)

RELATIONSHIP_PATTERNS = [
    r'\b(\w+)\s+uses?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+manages?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+extends?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+contains?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+handles?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+communicates?\s+with\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+sends?\s+(?:\w+\s+)?(?:to\s+)?(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+stores?\s+(?:\w+\s+)*(?:from\s+)?(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+depends?\s+on\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+calls?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+accesses?\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+interacts?\s+with\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+delegates?\s+to\s+(?:the\s+)?(\w+)\b',
    r'\b(\w+)\s+connects?\s+to\s+(?:the\s+)?(\w+)\b',
]

def is_valid_srs_class(word: str) -> bool:
    if word in STOP_WORDS or word.lower() in {s.lower() for s in STOP_WORDS}:
        return False
    if len(word) < 4:
        return False
    if word.isupper() and len(word) <= 4:
        return False
    if not re.match(r'^[A-Z][a-zA-Z0-9]{2,}$', word):
        return False
    return True

def extract_srs_entities(srs_metni: str) -> dict:
    """SRS metninden varlıkları çıkarır — gelişmiş filtreli versiyon."""
    candidates = {}

    # Önce bilinen suffix'li sınıflar
    for suffix in CLASS_SUFFIXES:
        pattern = rf'\b([A-Z][a-zA-Z0-9]*{suffix})\b'
        for m in re.finditer(pattern, srs_metni):
            w = m.group(1)
            if is_valid_srs_class(w):
                candidates[w] = candidates.get(w, 0) + 3

    # CamelCase
    for m in re.finditer(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b', srs_metni):
        w = m.group(1)
        if is_valid_srs_class(w) and w not in candidates:
            candidates[w] = candidates.get(w, 0) + 2

    siniflar = set(candidates.keys())

    # İlişkiler
    class_lower = {c.lower(): c for c in siniflar}
    iliskiler = set()
    for pat in RELATIONSHIP_PATTERNS:
        for src_raw, tgt_raw in re.findall(pat, srs_metni, re.IGNORECASE):
            src = class_lower.get(src_raw.strip().lower())
            tgt = class_lower.get(tgt_raw.strip().lower())
            if src and tgt and src != tgt:
                iliskiler.add((src, tgt))

    return {"siniflar": siniflar, "iliskiler": iliskiler}


def extract_uml_entities(plantuml_kodu: str, legacy: bool = False) -> dict:
    """PlantUML kodundan varlıkları çıkarır."""
    tum_siniflar = parse_classes(plantuml_kodu, legacy=legacy)
    iliskiler = parse_relationships(plantuml_kodu, legacy=legacy)

    return {"siniflar": tum_siniflar, "iliskiler": iliskiler}


def hesapla_f1(tahmin: set, gercek: set) -> dict:
    """Precision, Recall ve F1 skoru hesaplar."""
    if not gercek and not tahmin:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if not gercek:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    def normalize(x):
        if isinstance(x, str):
            return x.lower()
        return "_".join(str(i).lower() for i in x)

    tahmin_n = {normalize(t) for t in tahmin}
    gercek_n = {normalize(g) for g in gercek}

    kesisim = len(tahmin_n & gercek_n)
    precision = kesisim / len(tahmin_n) if tahmin_n else 0.0
    recall = kesisim / len(gercek_n) if gercek_n else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) > 0 else 0.0)

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3)
    }


def calculate_semantic_fidelity(srs_metni: str, plantuml_kodu: str) -> dict:
    """
    IEEE/ISO 29148'den esinlenen proje içi semantik sadakat değerlendirmesi.

    Kriterler:
        C1 (0.35): Sınıf doğruluğu — F1 skoru
        C2 (0.25): İlişki doğruluğu — F1 skoru
        C3 (0.25): Bütünlük — eksik sınıf oranı
        C4 (0.15): Tutarlılık — halüsinasyon oranı
    """
    srs = extract_srs_entities(srs_metni)
    uml = extract_uml_entities(plantuml_kodu)

    sinif_metrik = hesapla_f1(uml["siniflar"], srs["siniflar"])
    iliski_metrik = hesapla_f1(uml["iliskiler"], srs["iliskiler"])

    uml_lower = {u.lower(): u for u in uml["siniflar"]}
    srs_lower = {s.lower() for s in srs["siniflar"]}

    halusinasyonlar = [uml_lower[u] for u in uml_lower if u not in srs_lower]
    eksik = [s for s in srs["siniflar"] if s.lower() not in uml_lower]

    c1 = sinif_metrik["f1"]
    c2 = iliski_metrik["f1"] if srs["iliskiler"] else 1.0
    c3 = 1.0 - (len(eksik) / len(srs["siniflar"])) if srs["siniflar"] else 1.0
    c4 = 1.0 - (len(halusinasyonlar) / len(uml["siniflar"])) if uml["siniflar"] else 1.0

    genel_skor = round((c1 * 0.35) + (c2 * 0.25) + (c3 * 0.25) + (c4 * 0.15), 3)

    return {
        "genel_skor": genel_skor,
        "yuzde": f"%{round(genel_skor * 100, 1)}",
        "sinif_metrikleri": sinif_metrik,
        "iliski_metrikleri": iliski_metrik,
        "halusinasyonlar": halusinasyonlar,
        "eksik_siniflar": eksik,
        "ieee_kriterleri": {
            "C1_sinif_dogrulugu": round(c1, 3),
            "C2_iliski_dogrulugu": round(c2, 3),
            "C3_butunluk": round(c3, 3),
            "C4_tutarlilik": round(c4, 3)
        },
        "gecti_mi": genel_skor >= 0.75
    }


if __name__ == "__main__":
    srs = """
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
    from srs_parser import srs_to_plantuml
    r = srs_to_plantuml(srs)
    print("Sınıflar:", r["bulunan_siniflar"])
    ev = calculate_semantic_fidelity(srs, r["plantuml_kodu"])
    print("Skor:", ev["yuzde"])
    print("Halüsinasyonlar:", ev["halusinasyonlar"])
    print("Eksik:", ev["eksik_siniflar"])
    print("Criteria:", ev["ieee_kriterleri"])
