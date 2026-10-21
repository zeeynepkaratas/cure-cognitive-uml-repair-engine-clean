import re

try:
    from utils.plantuml_parser import parse_relationships, parse_model
except ModuleNotFoundError:  # package import path: src.ocl_engine.ocl_validator
    from src.utils.plantuml_parser import parse_relationships, parse_model


class OCLKural:
    """OCL kuralı veri sınıfı."""

    def __init__(self, kod, aciklama, siddet="HATA"):
        self.kod = kod
        self.aciklama = aciklama
        self.siddet = siddet  # "HATA" veya "UYARI"


# Tanımlı OCL kuralları
OCL_KURALLARI = {
    "OCL-01": OCLKural("OCL-01", "@startuml etiketi eksik", "HATA"),
    "OCL-02": OCLKural("OCL-02", "@enduml etiketi eksik", "HATA"),
    "OCL-03": OCLKural("OCL-03", "Hic sinif tanimlanmamis", "HATA"),
    "OCL-04": OCLKural("OCL-04", "God Class: sinif cok fazla metot iceriyor (>10)", "UYARI"),
    "OCL-05": OCLKural("OCL-05", "Sinif isimlendirme kurali ihlali (PascalCase olmali)", "UYARI"),
    "OCL-06": OCLKural("OCL-06", "Izole sinif: hicbir iliskisi yok", "UYARI"),
    "OCL-07": OCLKural("OCL-07", "Dongusel bagimlilik tespit edildi", "UYARI"),
    "OCL-08": OCLKural("OCL-08", "Cok fazla sinif: diyagram karmasikligi yuksek (>20)", "UYARI"),
    "OCL-09": OCLKural("OCL-09", "Tekrar eden sinif ismi", "HATA"),
}


def parse_siniflar(plantuml_kodu: str) -> list:
    """PlantUML'den sınıf isimlerini çıkarır."""
    return [d.name for d in parse_model(plantuml_kodu).declarations]


def parse_iliskiler(plantuml_kodu: str) -> list:
    """PlantUML'den ilişkileri çıkarır."""
    return list(parse_relationships(plantuml_kodu))


def detect_cycle(siniflar: list, iliskiler: list) -> list:
    """Return every cyclic strongly connected component using Tarjan's method."""
    nodes = set(siniflar)
    graph = {n: set() for n in nodes}
    for source, target in iliskiler:
        if source in nodes and target in nodes:
            graph[source].add(target)
    index = 0
    stack, on_stack, indices, low, components = [], set(), {}, {}, []

    def visit(node):
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in sorted(graph[node]):
            if target not in indices:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in on_stack:
                low[node] = min(low[node], indices[target])
        if low[node] == indices[node]:
            component = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            if len(component) > 1 or node in graph[node]:
                components.append("SCC: {" + ", ".join(sorted(component)) + "}")

    for node in sorted(nodes):
        if node not in indices:
            visit(node)
    return sorted(components)


def validate_ocl(plantuml_kodu: str, legacy: bool = False) -> dict:
    """
    PlantUML diyagramını OCL kurallarına göre kapsamlı doğrular.

    Girdi:
        plantuml_kodu (str): Doğrulanacak PlantUML kodu

    Çıktı:
        dict:
            gecerli_mi    : bool  - Hiç kritik hata yok mu?
            skor          : float (0.0-1.0)
            yuzde         : str
            hatalar       : list  - Kritik ihlaller (siddet=HATA)
            uyarilar      : list  - Uyarılar (siddet=UYARI)
            sinif_sayisi  : int
            iliski_sayisi : int
            detaylar      : dict  - Her kural için sonuç
    """
    if legacy:
        from .ocl_validator_legacy import validate_ocl as legacy_validate

        return legacy_validate(plantuml_kodu)
    hatalar = []
    uyarilar = []
    detaylar = {}

    siniflar = parse_siniflar(plantuml_kodu)
    iliskiler = parse_iliskiler(plantuml_kodu)

    # OCL-01: @startuml kontrolü
    if "@startuml" not in plantuml_kodu:
        hatalar.append(OCL_KURALLARI["OCL-01"].aciklama)
        detaylar["OCL-01"] = "IHLAL"
    else:
        detaylar["OCL-01"] = "GECTI"

    # OCL-02: @enduml kontrolü
    if "@enduml" not in plantuml_kodu:
        hatalar.append(OCL_KURALLARI["OCL-02"].aciklama)
        detaylar["OCL-02"] = "IHLAL"
    else:
        detaylar["OCL-02"] = "GECTI"

    # OCL-03: En az 1 sınıf olmalı
    if len(siniflar) == 0:
        hatalar.append(OCL_KURALLARI["OCL-03"].aciklama)
        detaylar["OCL-03"] = "IHLAL"
    else:
        detaylar["OCL-03"] = "GECTI"

    # OCL-04: God Class tespiti
    god_classes = []
    for declaration in parse_model(plantuml_kodu).declarations:
        count = sum(
            bool(re.match(r"^[+\-#~]?\s*[A-Za-z_]\w*\s*\(", method))
            and not method.lstrip().startswith(("if ", "if(", "while", "for ", "for("))
            for method in declaration.methods
        )
        if count > 10:
            god_classes.append(f"{declaration.name} ({count} methods)")
    if god_classes:
        uyarilar.append(f"{OCL_KURALLARI['OCL-04'].aciklama}: {', '.join(god_classes)}")
        detaylar["OCL-04"] = f"UYARI: {god_classes}"
    else:
        detaylar["OCL-04"] = "GECTI"

    # OCL-05: PascalCase isimlendirme
    yanlis_isim = [s for s in siniflar if not re.match(r"^[A-Z][a-zA-Z0-9]*$", s)]
    if yanlis_isim:
        uyarilar.append(f"{OCL_KURALLARI['OCL-05'].aciklama}: {yanlis_isim}")
        detaylar["OCL-05"] = f"UYARI: {yanlis_isim}"
    else:
        detaylar["OCL-05"] = "GECTI"

    # OCL-06: İzole sınıf tespiti
    iliskili_siniflar = set()
    for src, tgt in iliskiler:
        iliskili_siniflar.add(src)
        iliskili_siniflar.add(tgt)
    iliskili_lower = {i.lower() for i in iliskili_siniflar}
    izole = [s for s in siniflar if s.lower() not in iliskili_lower and len(siniflar) > 1]
    if izole:
        uyarilar.append(f"{OCL_KURALLARI['OCL-06'].aciklama}: {izole}")
        detaylar["OCL-06"] = f"UYARI: {izole}"
    else:
        detaylar["OCL-06"] = "GECTI"

    # OCL-07: Döngüsel bağımlılık
    donguler = detect_cycle(siniflar, iliskiler)
    if donguler:
        uyarilar.append(f"{OCL_KURALLARI['OCL-07'].aciklama}: {donguler[:3]}")
        detaylar["OCL-07"] = f"UYARI: {donguler}"
    else:
        detaylar["OCL-07"] = "GECTI"

    # OCL-08: Karmaşıklık
    if len(siniflar) > 20:
        uyarilar.append(f"{OCL_KURALLARI['OCL-08'].aciklama}: {len(siniflar)} sinif")
        detaylar["OCL-08"] = f"UYARI: {len(siniflar)} sinif"
    else:
        detaylar["OCL-08"] = "GECTI"

    # OCL-09: Tekrarlı isim
    tekrar = [s for s in siniflar if siniflar.count(s) > 1]
    if tekrar:
        hatalar.append(f"{OCL_KURALLARI['OCL-09'].aciklama}: {list(set(tekrar))}")
        detaylar["OCL-09"] = f"IHLAL: {tekrar}"
    else:
        detaylar["OCL-09"] = "GECTI"

    # Skor hesaplama
    ihlal_sayisi = len(hatalar)
    uyari_sayisi = len(uyarilar)
    skor = max(0.0, 1.0 - (ihlal_sayisi * 0.2) - (uyari_sayisi * 0.05))

    return {
        "gecerli_mi": len(hatalar) == 0,
        "skor": round(skor, 3),
        "yuzde": f"%{round(skor * 100, 1)}",
        "hatalar": hatalar,
        "uyarilar": uyarilar,
        "sinif_sayisi": len(siniflar),
        "iliski_sayisi": len(iliskiler),
        "detaylar": detaylar,
    }


if __name__ == "__main__":
    test_uml = """
    @startuml
    class UserManager {
        +login()
        +logout()
        +register()
    }
    class DiagramService {
        +generate()
        +validate()
    }
    class ValidationEngine {}
    UserManager --> DiagramService
    DiagramService --> ValidationEngine
    @enduml
    """
    r = validate_ocl(test_uml)
    print(f"Gecerli: {r['gecerli_mi']}")
    print(f"Skor: {r['yuzde']}")
    print(f"Hatalar: {r['hatalar']}")
    print(f"Uyarilar: {r['uyarilar']}")
