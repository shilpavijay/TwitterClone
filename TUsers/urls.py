from django.urls import path
from . import views
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('', views.landing),
    # path('api/users/', views.users),
    # path('api/users/<int:pk>/', views.user_details),
    # path('api/add_user/', views.add_user),
]