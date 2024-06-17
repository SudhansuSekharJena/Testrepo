from rest_framework.decorators import api_view # decorator

from rest_framework.response import Response

from rest_framework.views import APIView # class

from rest_framework import viewsets # imported for model view set.

from .serializers import *
from .models import * # Model / Database has been imported...

from django.contrib.auth.models import User

# Create your views here.


# @api_view(here list of methods will be here..means this function supprt which methods will be listed here)->IN THIS LIST EVERY METHOD WILL BE LISTED IN THE FORM OF STRING.

# @api_view(['GET', 'PUT', 'POST'])
# url of our api will be like abc.com/api/something --> /api/something

@api_view(['GET', 'POST', 'PUT', 'PATCH']) #.. GET method ..
def index(request): # here we are getting the data.
  courses = {
    'course_name': 'Python', 
    'learn': ['flask', 'Django', 'Tornado', 'FastApi'],
    'course_provider': 'Scaler'
  }
  if request.method == 'GET': # request.method -> is for checking requested method -> [ GET, PUT, POST, PATCH ]
    # TO GET DATA FROM THE SERVER YOU CAN DO LIKE THIS. Here we will use Query parameter.
    print(request.GET.get('search')) # so here the Query parameter /?search=Sudhansu
    
    print('YOU HAVE REQUESTED FOR GET METHOD...')
    return Response(courses) # by using Response -> we can send data. 
  elif request.method == 'POST':
    
    data = request.data # this is used to get data when send from the server and will be used in put, pathc, post methods
    print('....The data sent from the frontend....')
    print(data)
    return Response('Your Data has been sent...')
  elif request.method == 'PUT':
    print('PUT METHOD HAS BEEN REQUESTED')
    return Response(courses)
  elif request.method == 'PATCH':
    print('PATCH METHOD HAS BEEN REQUESTED....')
    return Response(courses)
  
  
  # 'request.method'
  # 'request.data'--> request.data is an attribute of 'Request' object that contains the parsed data of the request body. This is used when handling incoming data from HTTP requests, particularly for methods like POST, PUT and PATCH, where the client sends data to be processed by the server.
  
# TO CREATE A API ALSO YOU HAVE TO CREATE A CLASS

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE']) # this converts the Django view to DRF View, enabling the use of DRF-specific request and Response  handling.

def person(request): # person is a view function takes HTTP request object as argument.
  if request.method=='GET':
    # objects = Person.objects.all() # -> it will return a list of fields from the model. 
    
    # Person.objects.all --> Person: Model, objects: manager, all(): method applied on Person Model by manager
    
    objects = Person.objects.filter(color__isnull = False) # filter out the persons whose color is not null
    
    # Serialize it...
    serializer = PersonSerializer(objects, many=True) # returns a querySet. # --> This will Serialize the contents of Person Model and the serialized data will be stored in serializer object.
    print('Notification got')
    return Response(serializer.data) # Returns a 'Response' object containing appropriate content.
  elif request.method == 'POST':
    data = request.data # 'request.data' contains the data sent by the client, parsed into a dictionary or a set depending on the content.
    serializer = PersonSerializer(data=data) # here as we get data from the client then here deserialiszation is going on with validing each and every data.
    
    # now vaildate the data
    if serializer.is_valid(): # Checking the provided data is valid or not to the serializer's rule.
      serializer.save() # if the data is valid, the serializer saves the new 'Person' instance to the database.
      print('Notification sent...')
      return Response(serializer.data)
    
    print('Some error happened...')
    return Response(serializer.errors)
  
  # here what happened:-
  # - GET request:- it retrieves all 'Person' instances, serialize them, and returns the serialized data.
   # RETRIEVE DATA -> SERIALIZE THE DATA -> RETURN THE SERIALIZED DATA.
  
  # - POST request:- it retrieves data from the request of  the client, validates and saves it, and returns the serialized data of the newly created instance. If validation fails, then return the validation error.
  elif request.method == 'PUT': # doesnot support partial updation.
    data = request.data
    obj = Person.objects.get(id=data['id']) 
    serializer = PersonSerializer(obj, data=data)
    
    if serializer.is_valid():
      serializer.save()
      
      return Response(serializer.data)
    
    return Response(serializer.errors)
  
  elif request.method=='PATCH': # support partial updation.
    data = request.data
    obj = Person.objects.get(id=data['id']) # access the id.
    serializer = PersonSerializer(obj, data=data, partial=True)
    
    if serializer.is_valid():
      serializer.save()
      
      return Response(serializer.data)
    
    return Response(serializer.errors)
  else:
    data = request.data 
    obj = Person.objects.get(id=data['id'])
    obj.delete()
    return Response({"message":"person deleted"})
  

@api_view(['POST'])
def login(request):
  data = request.data 
  serializer = LoginSerializer(data = data)
  
  if serializer.is_valid():
    data = serializer.validated_data
    print(data)
    return Response({"message": "success"})
    
  return Response(serializer.errors)




# USING API VIEW NOT API_VIEW DECORATOR...
class PersonAPI(APIView):
  
   def get(self, request):
     objects = Person.objects.filter(color__isnull=False) 
     serializer = PersonSerializer(objects)  
     return Response(serializer.data)
   
   def post(self, request):
     data = request.data 
     serializer = PersonSerializer(data)
     if serializer.is_valid():
       serializer.save()
       return Response({"message":"person added successfully"})
     return Response(serializer.errors)
   
   def put(self, request):
     data = request.data 
     obj = Person.objects.get(id=data['id'])
     serializer = PersonSerializer(obj, data=data)
     if serializer.is_valid():
       serializer.save()
       return Response({"message":"person added successfully"})
     return Response(serializer.errors)
   
   def patch(self, request):
     data = request.data 
     obj = Person.objects.get(id=data['id'])
     serializer = PersonSerializer(obj, data=data, partial=True)
     if serializer.is_valid():
       serializer.save()
       return Response({"message":"person added successfully"})
     return Response(serializer.errors)
   
   def delete(self, request):
     return Response({"message":"This is a delete method"})
   

# USING MODEL-VIEW-SETs....
class PersonViewSet(viewsets.ModelViewSet):
  serializer_class = PersonSerializer
  queryset = Person.objects.all()
  
  
#--------------|REGISTRATION API|--------------------
# using APIView

class RegisterAPI (APIView):
  
  def post(self, request):
    data = request.data
    serializer = RegisterSerializer(data=data)
