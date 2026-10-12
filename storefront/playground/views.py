from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
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
    
    # Products: inventory < 10 AND price < 20
    queryset18 = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # this is the same:
    queryset19 = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    
    # Products: inventory < 10 OR price < 20
    queryset20 = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # you can also use '~' for 'not' and '&' for 'and' instead of '|'
    
    # Products: invnetory = price
    queryset21 = Product.objects.filter(inventory=F('unit_price'))
    # 'collection__id' also works
    
    queryset22 = Product.objects.order_by('unit_price', '-title') 
    # default is ascending, adding '-' will make it descending
    queryset23 = Product.objects.order_by('unit_price', '-title').reverse()
    # reverse() will reverse the direction of the sort
    product1 = Product.objects.order_by('unit_price')[0] # sorts it and then returns the first object
    product2 = Product.objects.earliest('unit_price') # orders ascending and returns the first object
    product3 = Product.objects.latest('unit_price') # orders descending and returns the first object
    
    
    # search queryset api for more information
    
    return render(request, 'hello.html', { 'name' : 'Mosh', 'products': list(queryset20)})