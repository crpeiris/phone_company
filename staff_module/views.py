from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, Role
from store.models import Order, Product
from .permissions import IsHelpDesk, IsOrderManager, IsGeneralManager
from django.contrib.auth.decorators import login_required
from .forms import StaffRegistrationForm, ProductForm  # Corrected import
from django.contrib import messages  # To display success or error messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from store.models import Product  # Import Product model
from .forms import ProductForm  # Import ProductForm

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')  # Redirect to the same page after adding a new product
    else:
        form = ProductForm()
    return render(request, 'staff_module/add_product.html', {'form': form, 'button_label': 'Add New Product'})

def search_product(request):
    search_value = request.GET.get('search_value')
    if search_value:
        products = Product.objects.filter(id__icontains=search_value)
        results = [{'id': p.id, 'name': p.name} for p in products]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def get_product(request):
    search_value = request.GET.get('search_value')
    if search_value:
        try:
            product = Product.objects.get(id=search_value)  # Fetch the product with the given ID
            result = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category.name if product.category else '',
                'description': product.description,
                'more_info': product.more_info,
                'image': product.image.url,  # URL for the image
                'is_sale': product.is_sale,
                'sale_price': product.sale_price
            }
            return JsonResponse(result, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({}, safe=False)  # Return empty object if product does not exist
    return JsonResponse({}, safe=False)  # Return empty object if search_value is not provided


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('add_product')  # Redirect after updating
    else:
        form = ProductForm(instance=product)
    return render(request, 'staff_module/add_product.html', {'form': form, 'button_label': 'Update Product'})



@login_required
def view_orders(request):
    if not IsHelpDesk().has_permission(request, None):
        return redirect('unauthorized')  # Redirect to an error page
    orders = Order.objects.all()
    return render(request, 'staff_module/view_orders.html', {'orders': orders})

@login_required
def update_order(request, order_id):
    if not IsOrderManager().has_permission(request, None):
        return redirect('unauthorized')
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.pay_reference = request.POST['pay_reference']
        order.delivery_reference = request.POST['delivery_reference']
        order.save()
        return redirect('view_orders')
    return render(request, 'staff_module/update_order.html', {'order': order})


@login_required
def add_staff(request):
    if not IsGeneralManager().has_permission(request, None):
        return redirect('unauthorized')

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)  # Save the user but not commit to the database yet
            staff.set_password(form.cleaned_data['password1'])  # Set the password
            staff.save()

            # Assign the selected role to the new staff user
            role = form.cleaned_data['role']
            staff.role.add(role)

            return redirect('staff_list')
    else:
        form = StaffRegistrationForm()

    return render(request, 'staff_module/add_staff.html', {'form': form})

@login_required
def unauthorized(request):
    return render(request, 'staff_module/unauthorized.html')

def staff_dashboard(request):
    return render(request, 'staff_module/staff_dashboard.html')
