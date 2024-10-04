from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import IndexView, ContactsView, BaseView, AlbumView, ProdsView, ProductListView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, ProductDetailView, VersionUpdateView, CategoryCreateView, CategoryUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('base/', BaseView.as_view(), name='base'),
    path('album/', AlbumView.as_view(), name='album'),
    path('category/<int:pk>/', cache_page(60)(ProdsView.as_view()), name='prods'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:product_id>/version/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_edit'),
    path('category/new/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update')
]
