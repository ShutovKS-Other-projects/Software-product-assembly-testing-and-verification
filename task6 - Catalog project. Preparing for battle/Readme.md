# 📦 Каталог SSD‑дисков — Django 3.2 | PostgreSQL | Docker | pytest

## 📖 Описание

```bash
# Запуск в Docker
docker compose build
docker compose up -d

# Линт + форматирование
docker compose exec web sh -c "flake8 . --exclude=catalog_project,catalog/tests,catalog/migrations,catalog/management/commands/ && echo 'flake8: OK'"
````

---

## 🚀 Функционал

| Блок                | Что есть                                                          |
|---------------------|-------------------------------------------------------------------|
| **Роли**            | Админ, Товаровед, Менеджер, Гость (Django Groups / Permissions)   |
| **SSD**             | Базовая цена + опт (small / large)                                |
| **Cart / CartItem** | Менеджер собирает партии, видит только свои; админ — все          |
| **Админка**         | Инлайн‑позиции CartItem, фильтры, права                           |
| **Тесты**           | django.test + pytest‑style asserts, покрытие 90 %+                |
| **Скрипты сидов**   | `seed_catalog` (товары) + `seed_demo` (группы, юзеры, партии)     |
| **CI‑ready**        | flake8 0 ошибок ⇒ статус «OK», юнит‑тесты зелёные, coverage отчёт |

---

## 🛠️ Стек

* Python 3.12
* Django 3.2
* PostgreSQL 16‑alpine
* gunicorn + nginx
* flake8 | black | isort
* pytest / django.test
* Docker Compose

---

## 📂 Структура

```
├── catalog/                    # приложение
│   ├── management/commands/    # seed_catalog, seed_demo
│   ├── migrations/
│   └── tests/
├── catalog_project/            # настройки Django
├── docker-compose.yml          # prod + init‑job
├── Dockerfile
├── nginx/nginx.conf
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── pyproject.toml              # black / isort / flake8 конфиг
```

---

## ⚙️ Переменные окружения

| Переменная      | По умолчанию | Что делает                     |
|-----------------|--------------|--------------------------------|
| `DJANGO_SECRET` | `changeme`   | `SECRET_KEY`                   |
| `DEBUG`         | `0`          | В dev‑профиле выставляется `1` |
| `POSTGRES_*`    | см. `.env`   | доступ к БД                    |

Скопируй `.env.example` → `.env` и поправь значения.

---

## 🐳 Docker

### docker-compose.yml

* `db` — Postgres + healthcheck
* `init` — **одноразовый job**: `migrate && seed_*`
* `web` — gunicorn
* `nginx` — отдаёт статику и проксирует API
* `volumes`: `pg_data`, `static_volume`

### Запуск

```bash
# build + старт
docker compose build
docker compose --profile dev up -d

# логи
docker compose logs -f web
```

---

## 🏃‍♂️ Bare‑metal (без Docker, по старинке)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_catalog --number=100
python manage.py seed_demo
python manage.py runserver
```

---

## 🧪 Тесты и покрытие

```bash
# все
python manage.py test

# с coverage
coverage run manage.py test
coverage report -m
```

Тесты закрывают: права доступа, расчёт оптовых цен, изоляцию партий по owner’у, CRUD для SSD/Cart.

## 👥 Тестовые пользователи

| Роль      | Логин      | Пароль          |
|-----------|------------|-----------------|
| Админ     | `admin`    | `1234`          |
| Менеджер  | `manager1` | `QWERasdf1234)` |
| Товаровед | `clerk`    | `QWERasdf1234)` |
| Гость     | `guest`    | `QWERasdf1234)` |

---
