from django.shortcuts import render

# Create your views here.
def storehome(request):
    return render(request, 'store/storehome.html', {})
    return render(request, 'store/storehome.html', {})

# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'store/aboutus.html', {})

def reviews(request):
    return render(request, 'store/reviews.html', {})

