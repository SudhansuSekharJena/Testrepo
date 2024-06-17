from myapp.views import *

from django.contrib import admin
from django.urls import path, include

# for modelViewSet--------------
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'personss', PersonViewSet, basename='person')# r'personss' is url , Viewset class: PersonViewSet, basename='person'
urlpatterns = router.urls

#--------------------------------

urlpatterns = [
  # @api_view() -> url
  path('index/', index), # when index/-> url view API called.
  path('person/', person), # when person/ -> person API called.
  path('login/', login),
  
  # API_VIEW url
  path('persons/', PersonAPI.as_view()), # we need .as_view() infront of class-based view to make it callable view function.
  
  # VIEW-SETS url
  path('', include(router.urls))
  
]

