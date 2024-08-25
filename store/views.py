from django.shortcuts import render

# Create your views here.
def storehome(request):
    return render(request, 'storehome.html', {})

def aboutus(request):
    return render(request, 'aboutus.html', {})

