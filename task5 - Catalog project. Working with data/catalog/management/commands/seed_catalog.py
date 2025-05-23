﻿from decimal import Decimal

from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from catalog.models import SSD, Interface, FormFactor


class Command(BaseCommand):
    help = "Генерирует тестовые данные для SSD"
    fake = Faker(['en_US'])

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=50, help='Количество SSD для генерации')
        parser.add_argument('--clear', action='store_true', help='Очистить базу перед генерацией')

    def handle(self, *args, **options):
        if options['clear']:
            SSD.objects.all().delete()
            Interface.objects.all().delete()
            FormFactor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("База данных очищена"))

        # Создаем интерфейсы
        interfaces = ['SATA', 'NVMe']
        for interface in interfaces:
            Interface.objects.get_or_create(name=interface)

        # Создаем форм-факторы
        form_factors = ['2.5"', 'M.2']
        for form_factor in form_factors:
            FormFactor.objects.get_or_create(name=form_factor)

        seeder = Seed.seeder()
        seeder.faker = self.fake

        brands = ["Samsung", "Western Digital", "Kingston", "Crucial", "SanDisk", "Intel", "Seagate"]
        models = ["EVO", "Pro", "Blue", "Green", "Ultra", "Plus", "Extreme"]

        seeder.add_entity(SSD, options['number'], {
            'sku': lambda x: f"SSD{seeder.faker.unique.random_number(digits=8)}",
            'brand': lambda x: seeder.faker.random_element(brands),
            'model': lambda
                x: f"{seeder.faker.random_element(models)} {seeder.faker.random_element(['Pro', 'Plus', 'Ultra', 'X', 'Lite'])}"[
                   :50],
            'capacity_gb': lambda x: seeder.faker.random_element([250, 500, 1000, 2000, 4000]),
            'interface': lambda x: Interface.objects.order_by('?').first(),
            'form_factor': lambda x: FormFactor.objects.order_by('?').first(),
            'read_speed': lambda x: seeder.faker.random_int(500, 7000),
            'write_speed': lambda x: seeder.faker.random_int(400, 6000),
            'warranty_years': lambda x: seeder.faker.random_int(1, 5),
            'price': lambda x: Decimal(
                seeder.faker.random_int(2000, 30000) + Decimal(seeder.faker.random_int(0, 99)) / 100),
            'in_stock': lambda x: seeder.faker.boolean(chance_of_getting_true=75),
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Успешно создано {options['number']} SSD-дисков"))
