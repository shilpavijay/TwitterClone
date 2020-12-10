from django.urls import path
from . import views
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('signup', views.AccountSignup),
    path('<str:username>/account', views.AccountUpdate),
    path('auth', views.GetToken),
    path('<str:loggedin_user>/<str:user>/follow', views.FollowUser),
    path('<str:username>/followers', views.GetFollowers),
    path('<str:username>/following', views.GetFollowing),
    path('<str:username>/block', views.Block_user), 
    path('users',views.users),
]