FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
COPY ai_core/requirements.txt /app/ai_core/requirements.txt

RUN pip install --no-cache-dir -r /app/backend/requirements.txt \
    && pip install --no-cache-dir -r /app/ai_core/requirements.txt

COPY . /app

EXPOSE 8000
