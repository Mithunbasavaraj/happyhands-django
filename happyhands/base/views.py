from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegistrationForm
from django.contrib import messages
from . models import product,cart,order




def home(request):
    return render(request, "index.html")

def products(request):
    post=product.objects.all()
    print(post)
    content={
       "post":post
    }
    return render(request, "products.html",content)

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def as_view(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect("base:login")

def authView(request):
 if request.method == "POST":
  form = RegistrationForm(request.POST or None)
  if form.is_valid():
   form.save()
   messages.success(request, "Register Success")
   return redirect("base:login")
 else:
  form = RegistrationForm()
 return render(request, "registration/signup.html", {"form": form})



    
# create products
# display products
# product details
# add to cart
# checkout
# payment
# product search implementation
# testing
# seo 
# deployment
# testing
# go live