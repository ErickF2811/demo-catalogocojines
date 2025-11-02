# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Variables de entorno base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para paquetes Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Configurar Flask
ENV FLASK_APP=app.main:app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_ENV=production

# Puerto expuesto
EXPOSE 5000

# Comando de arranque
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
