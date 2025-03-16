from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegistrationForm


def home(request):
    return render(request, "index.html")

def products(request):
    return render(request, "products.html")

def as_view(request):
    logout(request)
    return redirect("base:login")

def authView(request):
 if request.method == "POST":
  form = RegistrationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = RegistrationForm()
 return render(request, "registration/signup.html", {"form": form})

#todo

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