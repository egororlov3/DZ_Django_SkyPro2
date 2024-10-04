from django.conf import settings
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from catalog.forms import ProductForm, VersionForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.models import Category, Product, Version
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from catalog.services import get_cached_categories


# Главная страница с выводом популярных продуктов
class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'object_list'

    def post(self, request, *args, **kwargs):
        return render(request, 'catalog/contacts.html')


# Страница "Контакты"
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


# Статическая страница "Base"
class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/base.html'


# Страница с альбомом категорий
class AlbumView(ListView):
    model = Category
    template_name = 'catalog/album.html'
    context_object_name = 'object_list'
    extra_context = {'title': 'OrlovShop - наши товары'}


# Страница с товарами определенной категории
class ProdsView(LoginRequiredMixin, DetailView):
    template_name = 'catalog/prods.html'

    def get(self, request, pk, *args, **kwargs):
        category_item = get_object_or_404(Category, pk=pk)
        categories = get_cached_categories()

        context = {
            'object_list': Product.objects.filter(category_id=pk),
            'title': f'Наши товары - все товары {category_item.name}',
            'categories': categories
        }

        return render(request, self.template_name, context)


# Редактирование категории
class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'catalog.change_category'
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:album')


# Создание категории
class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'catalog.add_category'
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:album')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


# Просмотр всех товаров
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.prefetch_related('versions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            product.current_version = product.versions.filter(is_current=True).first()
        return context


# Просмотр определенного товара
@method_decorator(cache_page(60), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product_detail'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f'product_detail_{self.object.pk}'
            product_versions = cache.get(key)
            if product_versions is None:
                product_versions = self.object.versions.all()
                cache.set(key, product_versions)
        else:
            product_versions = self.object.versions.all()

        context_data['products'] = product_versions
        return context_data


# Создание товара
class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


# Редактирование товара
class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


# Удаление товара
class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = '/products/'
    permission_required = 'catalog.delete_product'


# Редактирование вресии товара
class VersionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.change_version'
    template_name = 'version_form.html'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('product_id')
        version_id = self.kwargs.get('pk')
        return get_object_or_404(Version, pk=version_id, product__id=product_id)

    def form_valid(self, form):
        version = form.save(commit=False)
        version.save()
        return redirect(reverse('catalog:product_detail', args=[version.product.id]))
