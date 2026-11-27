from python:3.11-slim

WORKDIR /frontend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
#ENTRENA Y GENERA EL ARTEFACTO EN BUILD
CMD  gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8001} 