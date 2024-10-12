from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm
from django import forms

# Create your views here.
def storehome(request):
    product = Product.objects.all()
    return render(request, 'store/storehome.html', {'products': product})

# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'store/aboutus.html', {})

def reviews(request):
    return render(request, 'store/reviews.html', {})


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
        return render( request, 'store/login.html', {})


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
        return render(request,'store/register.html', {'form': form})
