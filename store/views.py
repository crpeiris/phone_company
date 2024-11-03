from datetime import datetime
from django.shortcuts import render, redirect
from .models import CartItem, Product,Category,Order,OrderProduct
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


# Create your views here.
def storehome(request):
    return render(request, 'store/storehome.html', {'title': 'Next Gen Phone Shop'})


# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'store/aboutus.html', {'title': 'About us'})

def reviews(request):
    return render(request, 'store/reviews.html', {'title': 'Customer Reviews'})


def login_user(request):
    if request.method == "POST":
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been Logged in..."))
            return redirect ('storehome')
        else:
            messages.success(request, ("Username or Password incorrect...Please try again"))
            return redirect ('login_user')
    else:
        return render( request, 'store/login.html', {'title': 'Sign in'})


def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out...Thank you!'))
    return redirect('storehome')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data["username"]
            password= form.cleaned_data["password1"]
            #log in user
            user =authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have registered! Welcome !!!"))
            return redirect('storehome')
        else:
            messages.success(request, ("threre is a problem registering, try agaian"))
            return redirect('storehome')
    else:
        return render(request,'store/register.html', {'form': form, 'title': 'Join with us'})

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

def add_to_cart(request, product_id):
    if request.user :
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop')

def view_cart(request):
    if request.user.is_anonymous:
        pass
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.sale_price * item.quantity for item in cart_items)
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Shopping Cart'})

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

            order_items = OrderProduct.objects.filter(order_id = new_order.id)
            total_price = sum(purchase.product.sale_price * purchase.quantity for purchase in order_items)
            return render(request, 'store/order.html', {'order_items': order_items, 'total_price': total_price, 'title': 'Order Preview'})

        except Exception as e:
           print ("error creating order : " , e)
           return redirect('view_cart') 

