"""
URL configuration for djangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from eshop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name="main"),
    path('laptops/', laptops, name="laptops"),
    path('phones/', phones, name="phones"),
    path('tvs/', tvs, name="tvs"),
    path("product/add/", add, name="add"),
    path("products/", products, name="products"),
    path("dashboard/", homeadmin, name="dashboard"),
    path("customer/<str:pk>/", customer, name="customer"),
    path("update_order/<str:pk>/", updateOrder, name="update_order"),
    path("delete_order/<str:pk>/", deleteOrder, name="delete_order"),
    path("register/", registerPage, name="register"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("update_product/<str:pk>/", updateProduct, name="update_product"),
    path("delete_product/<str:pk>/", deleteProduct, name="delete_product"),
    path("delete_customer/<str:pk>/", deleteCustomer, name="delete_customer"),
    path("add_to_cart/<str:pk>/", add_to_cart, name="add_to_cart"),
    path("deleteCartItem/<str:pk>/", deleteCartItem, name="delete_cart_item"),
    path("cart/", cart_view, name="cart"),
    path("checkout/", checkout, name="checkout"),
   ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
