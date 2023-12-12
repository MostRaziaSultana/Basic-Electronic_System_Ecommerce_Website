from django.urls import path

from .views import *

urlpatterns = [
    path('product/<int:id>/', product, name='product'),
    path('single_product/<int:id>/', single_product, name='single_product'),
    path('addtoCart/<int:id>/', addtoCart, name='addtoCart'),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('minus_cart/<int:id>/', minus_cart, name='minus_cart'),
    path('plus_cart/<int:id>/', plus_cart, name='plus_cart'),
    path('sslcomerz/', sslcomerz, name='sslcomerz'),
    path('success/', success, name='success'),
    path('fail/', fail, name='fail'),
]
