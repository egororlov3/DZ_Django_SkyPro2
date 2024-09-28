from django.shortcuts import render

from catalog.models import Category, Product


def index(request):
    products = Product.objects.all()
    if request.method == 'POST':
        return render(request, 'catalog/contacts.html')
    return render(request, 'catalog/index.html', {'object_list': products})


def contacts(request):
    return render(request, 'catalog/contacts.html')


def base(request):
    return render(request, 'catalog/base.html')


def album(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'OrlovShop - наши товары'
    }
    return render(request, 'catalog/album.html', context)


def prods(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'Наши товары - все товары {category_item.name}'
    }
    return render(request, 'catalog/prods.html', context)
