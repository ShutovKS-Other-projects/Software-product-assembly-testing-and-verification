from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from catalog.admin import CartAdmin
from catalog.models import Cart


class MockSuperUser:
    is_superuser = True

    def __init__(self, user):
        self.pk = user.pk


class MockUser:
    is_superuser = False

    def __init__(self, user):
        self.pk = user.pk


class CartAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        User = get_user_model()
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'pass')
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass')
        self.cart1 = Cart.objects.create(owner=self.user1)
        self.cart2 = Cart.objects.create(owner=self.user2)
        self.admin = CartAdmin(Cart, self.site)

    def test_get_queryset_superuser(self):
        request = self.factory.get('/')
        request.user = self.superuser
        qs = self.admin.get_queryset(request)
        self.assertIn(self.cart1, qs)
        self.assertIn(self.cart2, qs)

    def test_get_queryset_user(self):
        request = self.factory.get('/')
        request.user = self.user1
        qs = self.admin.get_queryset(request)
        self.assertIn(self.cart1, qs)
        self.assertNotIn(self.cart2, qs)

    def test_has_change_permission_superuser(self):
        request = self.factory.get('/')
        request.user = self.superuser
        self.assertTrue(self.admin.has_change_permission(request, self.cart1))
        self.assertTrue(self.admin.has_change_permission(request, self.cart2))

    def test_has_change_permission_user(self):
        request = self.factory.get('/')
        request.user = self.user1
        self.assertTrue(self.admin.has_change_permission(request, self.cart1))
        self.assertFalse(self.admin.has_change_permission(request, self.cart2))

    def test_has_delete_permission_superuser(self):
        request = self.factory.get('/')
        request.user = self.superuser
        self.assertTrue(self.admin.has_delete_permission(request, self.cart1))
        self.assertTrue(self.admin.has_delete_permission(request, self.cart2))

    def test_has_delete_permission_user(self):
        request = self.factory.get('/')
        request.user = self.user1
        self.assertTrue(self.admin.has_delete_permission(request, self.cart1))
        self.assertFalse(self.admin.has_delete_permission(request, self.cart2))
