from store .models import Category, CartItem

def categories(request):
    categories = Category.objects.all()
    return {'categoryies': categories}

def cart_items_context(request):
    if request.user.is_anonymous:
        return {'cart_items_count': 0}
    else:
        cart_items_count = CartItem.objects.filter(user=request.user).count()
        return {'cart_items_count': cart_items_count}
