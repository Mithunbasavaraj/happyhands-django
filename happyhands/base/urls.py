from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("products/",views.products, name="products"),
    path("about/",views.about, name="about"),
    path("contact/",views.contact, name="contact"),
    path("signup/",views.authView, name="authView"),
    path("accounts/",include("django.contrib.auth.urls")),
    path('product-details/<slug:slug>/<int:pk>', views.product_details, name='product_details'),
    path('cart-page/', views.cart_page, name='cart_page'),
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add_to_cart'),

    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('qty-add/<int:pk>', views.qty_add, name='qty_add'),
    path('qty-sub/<int:pk>', views.qty_sub, name='qty_sub'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('order-details//<int:pk>', views.order_details, name='order_details'),
    path('admin-order-view/', views.admin_order_view, name='admin_order_view'),
    path('payment-return/', views.payment_return, name='payment_return'),
    path('pay/', views.pay, name='pay'),
    path('order-success/', views.order_success, name='order_success'),

]
