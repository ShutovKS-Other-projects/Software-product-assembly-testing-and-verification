# ./Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# collectstatic на слое build, чтобы не тормозить при run
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "catalog_project.wsgi:application", "-b", "0.0.0.0:8000", "-w", "4", "--timeout", "60"]
