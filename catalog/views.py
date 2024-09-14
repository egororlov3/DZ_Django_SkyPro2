from django.shortcuts import render


def index(request):
    if request.method == 'POST':
       return render(request, 'catalog/contacts.html')
    return render(request, 'catalog/index.html')

def contacts(request):
    return  render(request, 'catalog/contacts.html')
