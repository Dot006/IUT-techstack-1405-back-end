from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Customer, Order, OrderItem

def say_hello(request):
    # query_set = Product.objects.all() # it returns a query set
    # product = Product.objects.get(pk=1) # it returns an object
    # exists = Product.objects.filter(pk=0).exists() # it returns boolean
    
    queryset1 = Product.objects.filter(unit_price=20)
    queryset2 = Product.objects.filter(unit_price__gt=20)
    queryset3 = Product.objects.filter(unit_price__gte=20)
    queryset4 = Product.objects.filter(unit_price__lt=20)
    queryset5 = Product.objects.filter(unit_price__lte=20)
    queryset6 = Product.objects.filter(unit_price__range=(20, 30))
    queryset7 = Product.objects.filter(collection__id__range=(1, 2, 3))
    queryset8 = Product.objects.filter(title__icontains='coffee')
    queryset9 = Product.objects.filter(title__startswith='coffee')
    queryset10 = Product.objects.filter(title__endswith='coffee')
    queryset11 = Product.objects.filter(last_update__year=2021)
    queryset12 = Product.objects.filter(description__isnull=True)
    queryset13 = Customer.objects.filter(email__icontains='.com')
    queryset14 = Product.objects.filter(collection__featured_product__isnull=True)
    queryset15 = Product.objects.filter(inventory__lt=10)
    queryset16 = Order.objects.filter(customer__id=1)
    queryset17 = OrderItem.objects.filter(product__collection__id=3)
    # search queryset api for more information
    
    
    
    return render(request, 'hello.html', { 'name' : 'Mosh', 'products': list(queryset15)})