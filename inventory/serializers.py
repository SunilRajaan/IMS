from rest_framework import serializers 
from .models import ProductType, Department, Product, Vendor
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name'] 

    def create(self, validated_data):
        raw_password = validated_data.pop('password') # removed and assigned password key and value which user sent and validated
        hash_password = make_password(raw_password) # Hashing user's password using make_password
        validated_data['password'] = hash_password # passing the validated data onto create logic
        return super().create(validated_data)

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'