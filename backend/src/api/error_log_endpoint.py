"""
CP2 - /error-log endpoint'i
Hata geçmişini kaydeder ve sorgular.
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

router = APIRouter(prefix="/api", tags=["error-log"])

# In-memory hata log deposu (sunum için yeterli)
_hata_loglari: List[dict] = []

class HataLogGirdisi(BaseModel):
    kategori: str = Field(..., description="SYNTAX / OCL / SEMANTIC / HALLUCINATION")
    mesaj: str = Field(..., description="Hata mesajı")
    plantuml_kodu: Optional[str] = Field(None, description="İlgili UML kodu")
    iterasyon_no: Optional[int] = Field(None, description="Hangi iterasyonda oluştu")
    skor: Optional[float] = Field(None, description="O anki OCL/semantik skoru")

class HataLogCevabi(BaseModel):
    log_id: str
    zaman: str
    kategori: str
    mesaj: str

@router.post("/error-log", response_model=HataLogCevabi)
def hata_kaydet(girdi: HataLogGirdisi):
    """Hata kaydı oluşturur ve depolar."""
    kayit = {
        "log_id": str(uuid.uuid4())[:8],
        "zaman": datetime.now().isoformat(),
        "kategori": girdi.kategori,
        "mesaj": girdi.mesaj,
        "plantuml_kodu": girdi.plantuml_kodu,
        "iterasyon_no": girdi.iterasyon_no,
        "skor": girdi.skor
    }
    _hata_loglari.append(kayit)
    return kayit

@router.get("/error-log")
def hatalari_getir(kategori: Optional[str] = None, son_n: int = 20):
    """Kayıtlı hataları listeler. Kategori filtresi opsiyonel."""
    sonuclar = _hata_loglari
    if kategori:
        sonuclar = [h for h in sonuclar if h["kategori"] == kategori]
    return {
        "toplam": len(sonuclar),
        "loglar": sonuclar[-son_n:]
    }

@router.delete("/error-log")
def loglari_temizle():
    """Tüm hata loglarını temizler."""
    _hata_loglari.clear()
    return {"mesaj": "Tüm loglar temizlendi"}
