from django.shortcuts import render
from .models import ProductType, Department, Product, Vendor
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductTypeSerializer, DepartmentSerializer, ProductSerializer,VendorSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request): 
        serializer = self.get_serializer(data=request.data)        # we use data instead of post in api level
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def update(self, request,pk):
        # try:
        #     queryset = Department.objects.get(id=pk)
        # except:
        #     return Response({"error": "No mactching data found"})

        queryset = self.get_object()
        
        serializer = self.get_serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, pk):
        queryset = self.get_object()
        
        serializer = self.get_serializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    def retrieve(self, request, pk):
        queryset = self.get_object()

        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        queryset = self.get_object()

        queryset.delete()
        return Response()
    
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            departments = request.data.get('departments', [])
            if departments:
                product.department.set(departments)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            departments = request.data.get('departments')
            if departments is not None:
                product.department.set(departments)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            departments = request.data.get('departments')
            if departments is not None:
                product.department.set(departments)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserApiView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def register(self, request):
        # request.data.get('password')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def login(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():  
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
        
            if user == None:
                return Response({"Error" : "Invalid credential"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                token,_ =Token.objects.get_or_create(user=user)
                return Response({'token':token.key})
        else:
            return 
