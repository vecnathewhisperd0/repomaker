from django.test import TestCase

from repomaker.migrations.default_categories import DEFAULT_CATEGORIES
from repomaker.models import Category


class CategoryTestCase(TestCase):

    def test_pre_install(self):
        categories = Category.objects.all()
        self.assertEqual(len(DEFAULT_CATEGORIES), len(categories))

        categoriesNames = [category[0] for category in DEFAULT_CATEGORIES]
        for c in categories:
            self.assertTrue(c.name in categoriesNames)

    def test_str(self):
        category = Category.objects.get(name=DEFAULT_CATEGORIES[0][0])
        self.assertEqual(category.name, str(category))

    def test_default_category_has_default_color(self):
        category = Category.objects.get(name=DEFAULT_CATEGORIES[0][0])
        self.assertEqual(category.color, DEFAULT_CATEGORIES[0][1])
