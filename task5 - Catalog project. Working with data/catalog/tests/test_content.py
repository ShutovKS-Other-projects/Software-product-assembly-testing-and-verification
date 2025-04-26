from django.test import TestCase

from catalog.models import SSD, Interface, FormFactor


class ContentTests(TestCase):
    def setUp(self):
        self.interface1 = Interface.objects.create(name="SATA")
        self.interface2 = Interface.objects.create(name="NVMe")
        self.form_factor1 = FormFactor.objects.create(name="2.5")
        self.form_factor2 = FormFactor.objects.create(name="M.2")

        # Создаем тестовые SSD с разными характеристиками
        self.ssd1 = SSD.objects.create(
            sku="TEST1",
            brand="Brand A",
            model="Model 1",
            capacity_gb=256,
            interface=self.interface1,
            form_factor=self.form_factor1,
            read_speed=500,
            write_speed=400,
            price=1000.00
        )

        self.ssd2 = SSD.objects.create(
            sku="TEST2",
            brand="Brand B",
            model="Model 2",
            capacity_gb=512,
            interface=self.interface2,
            form_factor=self.form_factor2,
            read_speed=3000,
            write_speed=2000,
            price=2000.00,
            warranty_years=5
        )

    def test_alphabetical_ordering(self):
        ssds = SSD.objects.all().order_by('brand', 'model')
        self.assertEqual(list(ssds), [self.ssd1, self.ssd2])

    def test_price_ordering(self):
        ssds = SSD.objects.all().order_by('price')
        self.assertEqual(list(ssds), [self.ssd1, self.ssd2])

    def test_capacity_ordering(self):
        ssds = SSD.objects.all().order_by('capacity_gb')
        self.assertEqual(list(ssds), [self.ssd1, self.ssd2])

    def test_interface_filtering(self):
        ssds = SSD.objects.filter(interface=self.interface1)
        self.assertEqual(list(ssds), [self.ssd1])

    def test_form_factor_filtering(self):
        ssds = SSD.objects.filter(form_factor=self.form_factor2)
        self.assertEqual(list(ssds), [self.ssd2])
