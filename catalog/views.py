from django.views import View
from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Category, Product


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
