from django.shortcuts import render
from .models import ProductType, Department
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .serializers import ProductTypeSerializer, DepartmentSerializer

# Create your views here.
# def home(request):
#     return render(request, 'home.html')
class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class DepartmentApiView(GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request): 
        serializer = self.get_serializer(data=request.data)        # we use data instead of post in api level
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    

