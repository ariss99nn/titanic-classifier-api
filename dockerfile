# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# evitar buffering en logs
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto; Railway/Cloud asignará PORT env var
EXPOSE 8000

# usar sh -c para permitir expansion de ${PORT}
ENTRYPOINT ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]