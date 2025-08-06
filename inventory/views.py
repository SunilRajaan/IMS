from django.shortcuts import render
from django.db.models import Sum, Avg
from .models import ProductType, Department, Product, Vendor, Sell, Purchase, Rating
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductTypeSerializer, DepartmentSerializer, ProductSerializer,VendorSerializer, UserSerializer, LoginSerializer, SellSerializer, PurchaseSerializer, RatingSerializer, GroupSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import User, Group 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .ai import generate_product_description
from rest_framework.decorators import action

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
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'], url_path='generate-description')
    def generate_description(self, request):
        product_name = request.data.get('name')
        if not product_name:
            return Response(
                {"error": "Product name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        description = generate_product_description(product_name)
        return Response(
            {"name": product_name, "description": description},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        # If description is empty, generate one automatically
        if not request.data.get('description'):
            product_name = request.data.get('name')
            if product_name:
                try:
                    description = generate_product_description(product_name)
                    request.data._mutable = True
                    request.data['description'] = description
                    request.data._mutable = False
                except Exception as e:
                    print(f"Failed to generate description: {e}")
        
        return super().create(request, *args, **kwargs)

    def best_selling(self, request):
        queryset = Product.objects.all().annotate(total_sell_quantity=Sum('sells__quantity')).order_by('-total_sell_quantity')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def most_purchased(self, request):
        queryset = Product.objects.all().annotate(total_purchased_quantity=Sum('purchases__quantity')).order_by('-total_purchased_quantity')
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    def top_rated(self, request):
        queryset = Product.objects.all().annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         product = serializer.save()
    #         departments = request.data.get('departments', [])
    #         if departments:
    #             product.department.set(departments)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     if serializer.is_valid():
    #         product = serializer.save()
    #         departments = request.data.get('departments')
    #         if departments is not None:
    #             product.department.set(departments)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         product = serializer.save()
    #         departments = request.data.get('departments')
    #         if departments is not None:
    #             product.department.set(departments)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellViewSet(ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer

class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer