from django.shortcuts import render
from .models import Product


# Create your views here.
def storehome(request):
    product = Product.objects.all()
    return render(request, 'store/storehome.html', {'products': product})

# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'store/aboutus.html', {})

def reviews(request):
    return render(request, 'store/reviews.html', {})

