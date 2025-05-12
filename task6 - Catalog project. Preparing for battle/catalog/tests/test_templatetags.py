from django.template import Context, Template
from django.test import RequestFactory, TestCase


class CustomTagsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_url_replace(self):
        request = self.factory.get('/?foo=1&bar=2')
        tpl = Template('{% load custom_tags %}{% url_replace foo=3 baz=4 %}')
        context = Context({'request': request})
        rendered = tpl.render(context)
        self.assertIn('foo=3', rendered)
        self.assertIn('bar=2', rendered)
        self.assertIn('baz=4', rendered)

    def test_param_replace(self):
        request = self.factory.get('/?foo=1&bar=2')
        tpl = Template('{% load param_replace %}{% param_replace request foo=3 baz=4 %}')
        context = Context({'request': request})
        rendered = tpl.render(context)
        self.assertIn('foo=3', rendered)
        self.assertIn('bar=2', rendered)
        self.assertIn('baz=4', rendered)
