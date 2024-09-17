from django.shortcuts import render

# Create your views here.
def storehome(request):
    return render(request, 'storehome.html', {})

# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'aboutus.html', {})

# This view return ‘reviews.html’ files.
def reviews(request):
    return render(request, 'reviews.html', {})
