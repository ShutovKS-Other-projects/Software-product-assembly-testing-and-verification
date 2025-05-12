from django.test import TestCase
from django.urls import reverse

from catalog.models import SSD, Interface, FormFactor


class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        interface = Interface.objects.create(name='SATA')
        form_factor = FormFactor.objects.create(name='2.5')
        SSD.objects.create(sku='sku1', brand='BrandA', model='ModelX', capacity_gb=256, interface=interface,
                           form_factor=form_factor, read_speed=500, write_speed=450, warranty_years=3, price=1000,
                           in_stock=True)
        SSD.objects.create(sku='sku2', brand='BrandB', model='ModelY', capacity_gb=512, interface=interface,
                           form_factor=form_factor, read_speed=550, write_speed=500, warranty_years=5, price=2000,
                           in_stock=False)

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')

    def test_home_view_search(self):
        response = self.client.get(reverse('home'), {'search': 'BrandA'})
        self.assertContains(response, 'BrandA')

    def test_home_view_filter_interface(self):
        response = self.client.get(reverse('home'), {'interface': 'SATA'})
        self.assertEqual(response.status_code, 200)

    def test_home_view_sort(self):
        response = self.client.get(reverse('home'), {'sort': 'price'})
        self.assertEqual(response.status_code, 200)

    def test_home_view_sort_invalid(self):
        response = self.client.get(reverse('home'), {'sort': 'invalid_field'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')

    def test_detail_view(self):
        ssd = SSD.objects.first()
        response = self.client.get(reverse('detail', args=[ssd.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/detail.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/about.html')
