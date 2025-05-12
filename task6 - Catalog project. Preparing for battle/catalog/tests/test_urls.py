from django.test import TestCase
from django.urls import reverse

from catalog.models import SSD, Interface, FormFactor


class UrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        interface = Interface.objects.create(name='SATA')
        form_factor = FormFactor.objects.create(name='2.5')
        cls.ssd = SSD.objects.create(sku='sku1', brand='BrandA', model='ModelX', capacity_gb=256, interface=interface,
                                     form_factor=form_factor, read_speed=500, write_speed=450, warranty_years=3,
                                     price=1000, in_stock=True)

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_detail_url(self):
        response = self.client.get(reverse('detail', args=[self.ssd.pk]))
        self.assertEqual(response.status_code, 200)

    def test_about_url(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        response = self.client.get('/admin/', follow=True)
        self.assertIn(response.status_code, [200, 302])
