from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.

def cart_summary(reqest):
    return render(reqest, 'cart/cart_summary.html', {})

def cart_add(reqest):
    #Get the cart from request
    cart=Cart(reqest)
    #test wether the request is post
    if reqest.POST.get('action') == 'post':
        #Get product id from the request
        product_id= int(reqest.POST.get('product_id'))
        #Search product in the database
        product= get_object_or_404(Product, id=product_id)
        # Add the product as an object to the session  
        cart.add(product=product)
        #Return a response
        response = JsonResponse({'Product Name ':product.name})
        return response

def cart_delete(reqest):
    #return render(reqest, 'cart/cart_delete.html', {})
    pass

def cart_update(reqest):
    #return render(reqest, 'cart/cart_update.html', {})
    pass
