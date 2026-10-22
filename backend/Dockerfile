FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends default-jre-headless graphviz curl ca-certificates && rm -rf /var/lib/apt/lists/*
COPY requirements.lock.txt /app/requirements.lock.txt
RUN pip install --no-cache-dir -r requirements.lock.txt
COPY tools/setup_plantuml.sh /app/tools/setup_plantuml.sh
RUN sed -i '1s/^\xEF\xBB\xBF//;s/\r$//' /app/tools/setup_plantuml.sh && sh /app/tools/setup_plantuml.sh
ENV PLANTUML_JAR=/opt/plantuml/plantuml.jar
COPY . /app
EXPOSE 8000
CMD ["uvicorn", "backend.src.api.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
