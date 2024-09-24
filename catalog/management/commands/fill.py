from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category1 = Category.objects.create(name='Категория 1', description='Описание категории 1')
        category2 = Category.objects.create(name='Категория 2', description='Описание категории 2')
        category3 = Category.objects.create(name='Категория 3', description='Описание категории 3')

        Product.objects.create(name='Продукт 1', description='Описание Продукта 1', category=category1, price=10)
        Product.objects.create(name='Продукт 2', description='Описание Продукта 2', category=category2, price=15)
        Product.objects.create(name='Продукт 3', description='Описание Продукта 3', category=category3, price=50)
