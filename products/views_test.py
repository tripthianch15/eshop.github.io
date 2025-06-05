from django.shortcuts import render
from .models import Product


def index_view(request):
    print("index_view")
    return marketplace_view(request,'all')

def marketplace_view(request, slug):
    #Fetch the categories and products from the database
    context ={}
    products = Product.objects.all()
    context.update({'products':products})
    print("Context", context)
    return render(request, 'index.html',context)

