from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

def say_hello(request):
    query_set = Product.objects.all() # it returns a query set
    product = Product.objects.get(pk=1) # it returns an object
    exists = Product.objects.filter(pk=0).exists() # it returns boolean
    
    return render(request, 'hello.html', { 'name' : 'Mosh'})