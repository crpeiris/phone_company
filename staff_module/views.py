from django.shortcuts import render, redirect, get_object_or_404
from store.models import Order, Product,Category
from django.contrib import messages
from django.http import JsonResponse
from .forms import ProductForm


from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator



def staff_home(request):
    return render(request, 'staff_module/staff_home.html', {'title':'Staff Home'})

@permission_required('staff_module.add_product')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        more_info = request.POST.get('more_info')
        image = request.FILES.get('image')
        is_sale = request.POST.get('is_sale') == 'on'
        sale_price = request.POST.get('sale_price') or None

        # Retrieve the category by its ID
        try:
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist.')
            return redirect('add_product')
        
        # Create and save the product
        product = Product.objects.create(
            name=name,
            price=price,
            category=category_obj,
            description=description,
            more_info=more_info,
            image=image,
            is_sale=is_sale,
            sale_price=sale_price,
        )
        product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('add_product') 

    return render(request, 'staff_module/add_product.html') 


@permission_required('staff_module.change_product')
def edit_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_search_id')
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            form = ProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Product updated successfully!'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid product ID'})

    elif request.method == 'GET':
        return render(request, 'staff_module/edit_product.html')



def search_product_list(request):
    search_value = request.GET.get('search_value')
    if search_value:
        products = Product.objects.filter(id__startswith=search_value)
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

@permission_required('staff_module.add_user')
def add_user(request):
    return render(request, 'staff_module/add_user.html', {'title':'Add User'})

@permission_required('staff_module.change_user')
def edit_user(request):
    return render(request, 'staff_module/edit_user.html', {'title':'Edit User'})

@permission_required('staff_module.view_order')
def view_order(request):
    order_list = Order.objects.all()
    paginator = Paginator(order_list, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'staff_module/view_order.html', {'title':'View Order', "page_obj": page_obj})

