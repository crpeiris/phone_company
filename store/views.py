from django.shortcuts import render

# Create your views here.
def storehome(request):
    return render(request, 'store/storehome.html', {})

def aboutus(request):
    return render(request, 'store/aboutus.html', {})

