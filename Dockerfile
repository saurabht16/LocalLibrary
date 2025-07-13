# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=locallibrary.settings

CMD ["sh", "-c", "python manage.py migrate && python manage.py test catalog"]
