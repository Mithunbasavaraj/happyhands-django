from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("products/",views.products, name="products"),
    path("signup/",views.authView, name="authView"),
    path("accounts/",include("django.contrib.auth.urls")),

]
