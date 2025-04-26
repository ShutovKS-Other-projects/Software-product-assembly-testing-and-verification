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

    def test_search_by_brand(self):
        response = self.client.get(reverse('home'), {'search': 'Test Brand'})
        self.assertContains(response, self.ssd.brand)

    def test_filter_by_interface(self):
        response = self.client.get(reverse('home'), {'interface': self.interface.name})
        self.assertContains(response, self.ssd.brand)

    def test_filter_by_form_factor(self):
        response = self.client.get(reverse('home'), {'form_factor': self.form_factor.name})
        self.assertContains(response, self.ssd.brand)

    def test_filter_by_min_price(self):
        response = self.client.get(reverse('home'), {'min_price': 900})
        self.assertContains(response, self.ssd.brand)

    def test_filter_by_max_price(self):
        response = self.client.get(reverse('home'), {'max_price': 1100})
        self.assertContains(response, self.ssd.brand)

    def test_sort_by_model(self):
        response = self.client.get(reverse('home'), {'sort': 'model'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')

    def test_pagination(self):
        # Создаем еще 49 SSD для проверки пагинации
        for i in range(49):
            SSD.objects.create(
                sku=f"SKU{i}",
                brand="Brand",
                model=f"Model{i}",
                capacity_gb=128,
                interface=self.interface,
                form_factor=self.form_factor,
                read_speed=100,
                write_speed=100,
                price=500.00
            )
        response = self.client.get(reverse('home'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')
