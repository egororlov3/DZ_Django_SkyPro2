from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from catalog.forms import ProductForm, VersionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Category, Product, Version


# Главная страница с выводом всех продуктов
class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'object_list'

    def post(self, request, *args, **kwargs):
        return render(request, 'catalog/contacts.html')


# Статическая страница "Контакты"
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


# Статическая страница "Base"
class BaseView(TemplateView):
    template_name = 'catalog/base.html'


# Страница с альбомом категорий
class AlbumView(ListView):
    model = Category
    template_name = 'catalog/album.html'
    context_object_name = 'object_list'
    extra_context = {'title': 'OrlovShop - наши товары'}


# Страница с товарами определенной категории
class ProdsView(View):
    template_name = 'catalog/prods.html'

    def get(self, request, pk, *args, **kwargs):
        category_item = Category.objects.get(pk=pk)
        context = {
            'object_list': Product.objects.filter(category_id=pk),
            'title': f'Наши товары - все товары {category_item.name}'
        }
        return render(request, self.template_name, context)


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product_detail'


# Создание продукта
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


# Редактирование продукта
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = '/products/'


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'version_form.html'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('product_id')
        version_id = self.kwargs.get('pk')
        return get_object_or_404(Version, pk=version_id, product__id=product_id)

    def form_valid(self, form):
        version = form.save(commit=False)
        version.save()
        return redirect(reverse('catalog:product_detail', args=[version.product.id]))
