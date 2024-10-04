from django.core.cache import cache
from .models import Category
from django.conf import settings


def get_cached_categories():
    """
    Получение списка категорий с кешированием.
    Если кеширование включено в настройках, то данные берутся из кеша.
    """
    key = 'categories_list'
    categories = cache.get(key)

    if categories is None:
        categories = Category.objects.all()
        if settings.CACHE_ENABLED:
            cache.set(key, categories, timeout=60)

    return categories
