from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import IndexView, ContactsView, BaseView, AlbumView, ProdsView

app_name = CatalogConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('base/', BaseView.as_view(), name='base'),
    path('album/', AlbumView.as_view(), name='album'),
    path('category/<int:pk>/', ProdsView.as_view(), name='prods'),
]

