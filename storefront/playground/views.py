from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Customer, Order, OrderItem
from tags.models import TaggedItem

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
    
    queryset24 = Product.objects.all()[:5] # 0, 1, 2, 3, 4
    queryset25 = Product.objects.all()[5:10] # 5, 6, 7, 8, 9
    
    queryset26 = Product.objects.values('id', 'title', 'collection__title') # only returns id and title field
    # values() returns a bunch of dictionaries 
    # .values_list() returns a bunch of tuples
    
    queryset27 = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    
    queryset28 = Product.objects.only('id', 'title') # with this, if you access another field, it'll query for it
    queryset29 = Product.objects.defer('description') # it'll return all the fields except 'description' field
    
    # select_related (1)
    # prefetch_related (n)
    queryset30 = Product.objects.prefetch_related('promotion').select_related('collection').all()
    # normally when you use 'objects.all()' it'll only query the product table, not related tables
    # with 'select_related' and 'prefetch_related' it'll preload related tables
    queryset31 = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    
    result = Product.objects.filter(collection__id=1).aggregate(count=Count('id'), min_price=Min('unit_price'))
    orderCount = Order.objects.aggregate(order_count=Count('id'))
    product1Sold = OrderItem.objects.filter(product__id=1).aggregate(product1Sold=Sum('quantity'))
    customer1OrderCount = Order.objects.filter(customer__id=1).aggregate(customer1OrderCount=Count('id'))
    collection3Products = Product.objects.filter(collection__id=3).aggregate(minPrice=Min('unit_price'), maxPrice=Max('unit_price'), avgPrice=Avg('unit_price'))
    
    queryset32 = Customer.objects.annotate(is_new=Value(True))
    queryset33 = Customer.objects.annotate(new_id=F('id') + 1)
    
    queryset34 = Customer.objects.annotate(
        full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    )
    # this is the same
    queryset35 = Customer.objects.annotate(
        full_name = Concat('first_name', Value(' '), 'last_name')
    )
    
    queryset36 = Customer.objects.annotate(orders_count=Count('order'))
    
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset37 = Product.objects.annotate(discounted_price=discounted_price)
    
    # search queryset api for more information
    
    content_type = ContentType.objects.get_for_model(Product)
    
    queryset38 = TaggedItem.objects\
        .select_related('tag')\
        .filter(
            content_type=content_type,
            object_id=1    
        )
    
    return render(request, 'hello.html', { 'name' : 'Mosh', 'tags': list(queryset38)})