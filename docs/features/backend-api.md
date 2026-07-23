# Backend API

## Aciklama

FastAPI tabanli CURE backend servisi SRS parse, UML render, OCL dogrulama,
semantik degerlendirme, hata loglama, performans raporu ve otonom onarim
endpointlerini yayinlar.

## Amac

Frontend ve deney scriptleri icin tek bir API kontrati saglamak.

## Kurulum

```bash
pip install -r backend/requirements.txt
pip install -r ai_core/requirements.txt
```

## Konfigurasyon

AI ajan akisi icin `ai_core/.env` icinde `OPENAI_API_KEY` tanimlanabilir.

## Kullanim

```bash
uvicorn backend.src.api.endpoints:app --reload --host 0.0.0.0 --port 8000
```

## Bagimliliklar

- fastapi
- uvicorn
- pydantic
- requests

## Dosya Yapisi

- `backend/src/api/endpoints.py`
- `backend/src/api/error_log_endpoint.py`
- `backend/src/api/performance.py`
- `backend/src/parsers/`
- `backend/src/ocl_engine/`
- `backend/src/renderers/`

## API

Ana endpointler:

- `POST /api/parse`
- `POST /api/render`
- `POST /api/validate`
- `POST /api/evaluate`
- `POST /api/analyze`
- `POST /api/autonomous-repair`
- `GET /api/performance`
- `GET /api/error-log`

## Veritabani Degisiklikleri

Yok. Hata loglari ve performans olcumleri prototipte bellek icinde tutulur.

## Test

```bash
python backend/tests/test_full.py
python backend/tests/test_api_contracts.py
```

## Hata Senaryolari

- Eksik PlantUML etiketleri compile testte yakalanir.
- Gecersiz SRS girdisi 400 veya guvenli hata yaniti uretir.
- AI ajan kullanilamazsa autonomous repair deterministik fallback healer ile devam eder.

## Gelistiren

Isim: CURE Team
Tarih: 2026-07-02

## Degisiklik Gecmisi

v1.0 - Backend API dokumantasyonu eklendi.
