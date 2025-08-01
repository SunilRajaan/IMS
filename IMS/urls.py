"""
URL configuration for IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from inventory.views import ProductTypeViewSet, DepartmentApiView, ProductViewSet, VendorViewSet, UserApiView, SellViewSet, PurchaseViewSet, RatingViewSet
urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/types/', ProductTypeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product/types/<int:pk>/', ProductTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("departments/",DepartmentApiView.as_view({'get':'list','post':'create'})),
    path("departments/<int:pk>/",DepartmentApiView.as_view({'get':'retrieve','patch':'partial_update','put':'update','delete':'destroy'})),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('best/selling/products/', ProductViewSet.as_view({'get': 'best_selling'})),
    path('products/generate/description/', ProductViewSet.as_view({'post': 'generate_description'})),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('vendors/', VendorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('vendors/<int:pk>/', VendorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('register/', UserApiView.as_view({'post': 'register'})),
    path('login/', UserApiView.as_view({'post': 'login'})),
    path('sell/', SellViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sell/<int:pk>/', SellViewSet.as_view({'get':'retrieve','patch':'partial_update','put':'update','delete':'destroy'})),
    path('purchases/', PurchaseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('purchases/<int:pk>/', PurchaseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('most/purchased/products/', ProductViewSet.as_view({'get': 'most_purchased'})),
    path('top/rated/products/', ProductViewSet.as_view({'get': 'top_rated'})),
    path('product/ratings/', RatingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product/ratings/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    ]
