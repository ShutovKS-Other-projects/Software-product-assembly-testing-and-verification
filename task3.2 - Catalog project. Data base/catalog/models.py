from django.db import models


class Interface(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Интерфейс")

    def __str__(self):
        return self.name


class FormFactor(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Форм-фактор")

    def __str__(self):
        return self.name


class SSD(models.Model):
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    brand = models.CharField(max_length=100, verbose_name="Производитель")
    model = models.CharField(max_length=100, verbose_name="Модель")
    capacity_gb = models.PositiveIntegerField(verbose_name="Ёмкость (ГБ)")
    interface = models.ForeignKey(Interface, on_delete=models.PROTECT, verbose_name="Интерфейс")
    form_factor = models.ForeignKey(FormFactor, on_delete=models.PROTECT, verbose_name="Форм-фактор")
    read_speed = models.PositiveIntegerField(verbose_name="Скорость чтения (МБ/с)")
    write_speed = models.PositiveIntegerField(verbose_name="Скорость записи (МБ/с)")
    warranty_years = models.PositiveIntegerField(null=True, blank=True, verbose_name="Гарантия (лет)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return f"{self.brand} {self.model}"
