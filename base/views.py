from django.shortcuts import render
from .models import ProductType
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductTypeSerializer

# Create your views here.
# def home(request):
#     return render(request, 'home.html')
class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
