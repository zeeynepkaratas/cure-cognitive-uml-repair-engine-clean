"""
CP4 - Performans olcum altyapisi.
Latency, SLA uyumu, basari orani ve P50/P95/P99 metriklerini hesaplar.
"""
import statistics
from typing import List, Optional
from datetime import datetime


SLA_LIMIT_SANIYE = 15.0

# Sunum ve test icin hafif in-memory olcum deposu.
# Gercek urun ortaminda burasi veritabani veya monitoring sistemi olabilir.
_olcumler: List[dict] = []


def olcum_kaydet(endpoint: str, sure_saniye: float, basarili: bool):
    """Her API cagrisinin suresini kaydeder."""
    _olcumler.append({
        "endpoint": endpoint,
        "sure": sure_saniye,
        "basarili": basarili,
        "zaman": datetime.now().isoformat(),
        "sla_gecti": sure_saniye < SLA_LIMIT_SANIYE
    })


def percentile_hesapla(veriler: List[float], p: float) -> float:
    """P50/P95/P99 gibi yuzdelik dilim hesaplar."""
    if not veriler:
        return 0.0
    sirali = sorted(veriler)
    index = int(len(sirali) * p / 100)
    return round(sirali[min(index, len(sirali) - 1)], 3)


def performans_raporu(endpoint: Optional[str] = None) -> dict:
    """
    Tum olcumler uzerinden P50/P95/P99 gecikme dagilimi raporu uretir.
    Makaleye veya CP4 sunumuna girecek tablo formatindadir.
    """
    veriler = _olcumler
    if endpoint:
        veriler = [o for o in veriler if o["endpoint"] == endpoint]

    if not veriler:
        return {"hata": "Henuz olcum yok", "toplam_istek": 0}

    sureler = [o["sure"] for o in veriler]
    basarili_sayisi = sum(1 for o in veriler if o["basarili"])
    sla_gecen = sum(1 for o in veriler if o["sla_gecti"])

    return {
        "toplam_istek": len(veriler),
        "basarili_istek": basarili_sayisi,
        "basari_orani": f"%{round(basarili_sayisi / len(veriler) * 100, 1)}",
        "sla_uyum_orani": f"%{round(sla_gecen / len(veriler) * 100, 1)}",
        "latency_ms": {
            "ortalama": round(statistics.mean(sureler) * 1000, 1),
            "P50": round(percentile_hesapla(sureler, 50) * 1000, 1),
            "P95": round(percentile_hesapla(sureler, 95) * 1000, 1),
            "P99": round(percentile_hesapla(sureler, 99) * 1000, 1),
            "min": round(min(sureler) * 1000, 1),
            "max": round(max(sureler) * 1000, 1),
        },
        "sla_siniri_saniye": SLA_LIMIT_SANIYE,
        "endpoint_filtresi": endpoint or "tumu"
    }


def olcumleri_sifirla():
    """Demo sirasinda temiz performans raporu almak icin olcumleri sifirlar."""
    _olcumler.clear()
