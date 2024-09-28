from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contacts, album, prods

app_name = CatalogConfig.name


urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('album/', album, name='album'),
    path('<int:pk>/prod/', prods, name='prods')
]

