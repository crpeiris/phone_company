from store .models import Category

def categories(request):
    categories = Category.objects.all()
    return {'categoryies': categories}
