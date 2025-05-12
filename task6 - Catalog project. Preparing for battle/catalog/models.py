from django.conf import settings
from django.db import models


class Interface(models.Model):
    name = models.CharField(max_length=20,
                            unique=True,
                            verbose_name="Интерфейс")

    def __str__(self):
        return self.name


class FormFactor(models.Model):
    name = models.CharField(max_length=20,
                            unique=True,
                            verbose_name="Форм-фактор")

    def __str__(self):
        return self.name


class SSD(models.Model):
    sku = models.CharField(
        max_length=50, unique=True, verbose_name="Артикул")

    brand = models.CharField(
        max_length=100, verbose_name="Производитель")

    model = models.CharField(
        max_length=100, verbose_name="Модель")

    capacity_gb = models.PositiveIntegerField(
        verbose_name="Ёмкость (ГБ)")

    interface = models.ForeignKey(
        Interface, on_delete=models.PROTECT, verbose_name="Интерфейс")

    form_factor = models.ForeignKey(
        FormFactor, on_delete=models.PROTECT, verbose_name="Форм-фактор")

    read_speed = models.PositiveIntegerField(
        verbose_name="Скорость чтения (МБ/с)")

    write_speed = models.PositiveIntegerField(
        verbose_name="Скорость записи (МБ/с)")

    warranty_years = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Гарантия (лет)")

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена")

    in_stock = models.BooleanField(
        default=True, verbose_name="В наличии")

    small_wholesale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name="Цена за мелкий опт")

    small_wholesale_min_qty = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Мин. количество для мелкого опта")
    large_wholesale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name="Цена за крупный опт")
    large_wholesale_min_qty = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Мин. количество для крупного опта")

    def __str__(self):
        return f"{self.brand} {self.model}"


class Cart(models.Model):
    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("submitted", "Отправлена"),
        ("shipped", "Отгружена"),
    ]
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name="Менеджер")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft",
        verbose_name="Статус")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Партия #{self.id} ({self.owner})"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items",
        verbose_name="Партия")
    product = models.ForeignKey(
        SSD, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(
        verbose_name="Количество")
    price_at_add = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Цена на момент добавления")

    def __str__(self):
        return f"{self.product} x {self.quantity} (Партия {self.cart.id})"
