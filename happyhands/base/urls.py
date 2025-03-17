from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("products/",views.products, name="products"),
    path("about/",views.about, name="about"),
    path("contact/",views.contact, name="contact"),
    path("signup/",views.authView, name="authView"),
    path("accounts/",include("django.contrib.auth.urls")),

]
