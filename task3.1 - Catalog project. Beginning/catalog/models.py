from django.db import models


class SSD(models.Model):
    INTERFACE_TYPES = [
        ('SATA', 'SATA'),
        ('NVMe', 'NVMe PCIe'),
    ]
    FORM_FACTORS = [
        ('2.5"', '2.5"'),
        ('M.2', 'M.2'),
    ]

    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    brand = models.CharField(max_length=100, verbose_name="Производитель")
    model = models.CharField(max_length=100, verbose_name="Модель")
    capacity_gb = models.PositiveIntegerField(verbose_name="Ёмкость (ГБ)")
    interface = models.CharField(max_length=20, choices=INTERFACE_TYPES, verbose_name="Интерфейс")
    form_factor = models.CharField(max_length=20, choices=FORM_FACTORS, verbose_name="Форм-фактор")
    read_speed = models.PositiveIntegerField(verbose_name="Скорость чтения (МБ/с)")
    write_speed = models.PositiveIntegerField(verbose_name="Скорость записи (МБ/с)")
    warranty_years = models.PositiveIntegerField(null=True, blank=True, verbose_name="Гарантия (лет)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return f"{self.brand} {self.model}"
