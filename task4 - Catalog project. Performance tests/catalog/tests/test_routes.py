from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import SSD, Interface, FormFactor


class RoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.interface = Interface.objects.create(name="SATA")
        self.form_factor = FormFactor.objects.create(name="2.5")
        self.ssd = SSD.objects.create(
            sku="TEST123",
            brand="Test Brand",
            model="Test Model",
            capacity_gb=256,
            interface=self.interface,
            form_factor=self.form_factor,
            read_speed=500,
            write_speed=400,
            price=1000.00
        )

    def test_catalog_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')
        self.assertContains(response, self.ssd.brand)

    def test_product_detail_page(self):
        response = self.client.get(reverse('detail', args=[self.ssd.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/detail.html')
        self.assertContains(response, self.ssd.brand)
        self.assertContains(response, self.ssd.model)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/about.html')
