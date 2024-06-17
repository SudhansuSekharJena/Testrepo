from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Color
    fields = ['color_name']
# Serializer classes inherit from serializers.ModelSerializer
class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    # The Meta class tells the serializer which model to use and which fields to include
    class Meta:
        model = Person  # This links the serializer to the Person model
        fields = '__all__'  # This tells the serializer to include all fields of the model
        
        # Alternatively, you can specify fields explicitly:
        # fields = ['name', 'age']
        
        # If you want to exclude specific fields, you can use:
        # exclude = ['field_to_exclude']
        depth = 1

      # VALIDATION FUNCTION WILL BE WRITTEN IN SERIALIZERS.PY
    def validate_age(self, data):# 1. name shouldnot have special characters. 2. age should be less than 18
      print('*********')
      print(data['age'])
      print(data['name'])
      print('*********')
      if data['age'] < 18:
        raise serializers.ValidationError('age should be greater than 18')
      return data
    
    def validate_name(self, data): # data is a dictionary
      special_characters = "!@#$%^&*()_+-=,<>/"
      
      # ...GOOD LOGIC...
      if any(c in special_characters for c in data['name']):
        raise serializers.ValidationError('name cannot contain any special characters')
      
      
      
#--------|REGISTER-SERIALIZER|------------
      
class RegisterSerializer(serializers.Serializer):
  # need username. email, password for registration Serializer
  username = serializers.CharField()
  email = serializers.EmailField()
  password = serializers.CharField()
  
  # Validation for checking the user is already present in the database or not.
  
  def validate_user(self, data): # data is the dictionary contains user info.
    if data['username']:
      if User.objects.filter(username=data['username']).exists():
        raise serializers.ValidationError('User already exists...')
      
    
    
        
      