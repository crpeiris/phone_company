from datetime import datetime
from django.shortcuts import render, redirect
from .models import CartItem, Product,Category,Order,OrderProduct
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def storehome(request):
    return render(request, 'store/storehome.html', {'title': 'Next Gen Phone Shop'})


# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'store/aboutus.html', {'title': 'About us'})

def reviews(request):
    return render(request, 'store/reviews.html', {'title': 'Customer Reviews'})


def shop(request, category = None):
    if category:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category=category)
        return render(request, 'store/shop.html', {'products': products, 'category' : category, 'title': category})
    else:
        products = Product.objects.all()
        return render(request, 'store/shop.html', {'products': products, 'category': 'all', 'title': 'All Phones' })

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product.html', {'product' : product, 'title': product.name })

#Views for Cartitems management

from django.contrib.auth.decorators import login_required
def add_to_cart(request, product_id):
    if request.user :
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop')

@login_required(login_url='login_user')
def view_cart(request):
    if request.user.is_anonymous:
        pass
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.sale_price * item.quantity for item in cart_items)
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Shopping Cart'})

from django.contrib.auth.decorators import login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@csrf_exempt  # Consider adding CSRF protection for production
def update_purchase(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        purchase_value = request.POST.get('purchase') == 'true'  # Convert to boolean

        try:
            item = CartItem.objects.get(id=item_id)
            item.purchase = purchase_value  # Update the purchase field
            item.save()
            return JsonResponse({'status': 'success'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@transaction.atomic
def create_order(request):
    if request.user.is_authenticated:
        try:
            new_order= Order.objects.create( customer=request.user, date=datetime.now().date())
            #order.address = request.user.address
            #order.phone = request.user.phone
            new_order.save()
    
            cart_items_purchase = CartItem.objects.filter(user=request.user , purchase=True)
            if cart_items_purchase:
                for item in cart_items_purchase:
                    product = Product.objects.get(id=item.product_id)  
                    soldprice = product.sale_price  
                    orderproduct = OrderProduct.objects.create(product= item.product, order= new_order)
                    orderproduct.quantity = item.quantity
                    orderproduct.soldprice= soldprice
                    orderproduct.save() 
                    item.delete() 

            order_items = OrderProduct.objects.filter(order_id = new_order.id)
            total_price = sum(purchase.product.sale_price * purchase.quantity for purchase in order_items)
            return render(request, 'store/order.html', {'order_items': order_items, 'total_price': total_price, 'title': 'Order Preview', 'orderid':new_order.id})

        except Exception as e:
           print ("error creating order : " , e)
           return redirect('view_cart') 

@transaction.atomic
def delete_order(request, order_id):
    if request.user.is_authenticated:
        try:
            order= Order.objects.get(id=order_id)
    
            order_items_delete = OrderProduct.objects.filter(order_id = order.id)
            if order_items_delete:
                for item in order_items_delete:
                    item.delete()       
        
            order.delete()
            messages.success(request,  f"Your Order {order_id} deleted. Please create a new order...")
            return redirect('view_cart')

        except Exception as e:
            messages.error(request,  f"Your Order {order_id} could not delete. Please contact support center...")
            return redirect('view_cart') 

