# Отчёт по заданию: Каталог товаров. Работа с данными

## Изменения и доработки

**Выполнено:**

- Добавлены роли пользователей (администратор, товаровед, менеджер, гость) через Django Groups/Permissions.
- В модель SSD добавлены поля для мелкого и крупного опта: `small_wholesale_price`, `small_wholesale_min_qty`,
  `large_wholesale_price`, `large_wholesale_min_qty`.
- Добавлены модели Cart (партия/корзина) и CartItem (позиция в партии) для формирования партий товаров менеджерами.
- В Django Admin:
    - Зарегистрированы Cart и CartItem.
    - Для CartAdmin реализовано ограничение: менеджер видит и может изменять только свои партии, администратор — все.
- В шаблоне каталога исправлены ошибки сравнения и дублирование номеров страниц.

**Пример кода моделей:**

```python
class SSD(models.Model):
    ...
    small_wholesale_price = models.DecimalField(...)
    small_wholesale_min_qty = models.PositiveIntegerField(...)
    large_wholesale_price = models.DecimalField(...)
    large_wholesale_min_qty = models.PositiveIntegerField(...)
    ...


class Cart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    status = models.CharField(...)
    created_at = models.DateTimeField(...)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, ...)
    product = models.ForeignKey(SSD, ...)
    quantity = models.PositiveIntegerField(...)
    price_at_add = models.DecimalField(...)
```

## Перечень тестов и описание проверки

- **Права доступа:**
    - Гость может только просматривать каталог.
    - Товаровед может редактировать только товары.
    - Менеджер может создавать и изменять только свои партии.
    - Администратор может всё.
- **Корректность изменения объектов каталога:**
    - Проверка создания, изменения и удаления товаров и партий.
- **Корректность расчёта суммы партии:**
    - Проверка расчёта стоимости с учётом оптовых цен и количества.
    - Проверка применения дополнительной скидки на общую сумму заказа.
- **Изоляция партий менеджеров:**
    - Один менеджер не может изменять партии другого.

**Пример описания теста:**

- "Тест создаёт двух менеджеров, каждый формирует свою партию. Проверяется, что менеджер №1 не видит и не может изменить
  партию менеджера №2."
- "Тест добавляет в корзину товар в количестве, превышающем порог для крупного опта, и проверяет, что применяется
  правильная цена."
- "Тест гость-пользователь пытается изменить товар — операция запрещена."

## Скриншоты

- Главная страница каталога с фильтрами и пагинацией
- Страница детали товара с оптовыми ценами
- Django Admin: список товаров (для товароведа)
- Django Admin: список партий (Cart) для менеджера (видны только свои партии)
- Django Admin: создание/редактирование партии (Cart + CartItem)
- Django Admin: настройка групп пользователей
- Проверка ограничения доступа (менеджер не видит чужие партии, товаровед не видит партии)

---

# Инструкция по запуску

```bash
# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py makemigrations
python manage.py migrate

# Заполнение базы тестовыми данными
python manage.py seed_catalog --number=100

# Генерация тестовых пользователей и партий
python manage.py seed_demo

# Запуск сервера
python manage.py runserver
```

**Доступ к админке:**  
<http://localhost:8000/admin/>

**Доступ пользователь:** таблица

| Логин    | Пароль        |
|----------|---------------|
| admin    | 1234          |
| manager1 | QWERasdf1234) |
| manager2 | QWERasdf1234) |
| clerk    | QWERasdf1234) |
| guest    | QWERasdf1234) |

---

### Добавление пользователей и групп

```powershell
# Создание суперпользователя
python manage.py createsuperuser
```

## Быстрая генерация тестовых пользователей, ролей и партий

Для автоматического создания тестовых пользователей с разными ролями, партий (Cart) и позиций (CartItem) используйте
команду:

```bash
python manage.py seed_demo
```

**Что будет создано:**

- Группы: Администратор, Товаровед, Менеджер, Гость
- Пользователи:
    - admin / adminpass (администратор, полный доступ)
    - manager1 / managerpass1 (менеджер)
    - manager2 / managerpass2 (менеджер)
    - clerk / clerkpass (товаровед)
    - guest / guestpass (гость)
- Для каждого менеджера будет создана тестовая партия с товарами (если товары уже есть в базе)

**Важно:** Сначала выполните генерацию товаров:

```bash
python manage.py seed_catalog --number=100
```

Затем выполните:

```bash
python manage.py seed_demo
```

После этого вы сможете войти под любым пользователем и проверить разграничение прав и работу партий в Django Admin.

---

## Запуск тестов

Для проверки корректности работы проекта и разграничения прав выполните тесты:

```bash
# Запуск всех тестов
python manage.py test

# Запуск тестов с измерением покрытия кода
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML-отчёт будет в папке htmlcov/
```

**Примеры запуска отдельных тестов:**

```bash
# Запуск конкретного теста
python manage.py test catalog.tests.test_routes.RoutesTests.test_catalog_page

# Запуск всех тестов в файле
python manage.py test catalog.tests.test_routes

# Запуск тестов с подробным выводом
python manage.py test catalog.tests -v 2
```

---
