from django.urls import path
# from TUsers.views import UserAPIView
from . import views
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('', views.Landing),
    path('login/', views.Authenticate),
    path('signup/', views.AccountSignup),
    path('users/',views.users),
    # path('', UserAPIView.Landing),
    # path('login', UserAPIView.Authenticate),
    # path('signup', UserAPIView.AccountSignup),
    # path('<str:username>/account', views.AccountUpdate),
    # path('auth', views.AuthToken),
    # path('<str:username>/follow', views.FollowUser),
    # path('<str:username>/followers', views.GetFollowers),
    # path('<str:username>/following', views.GetFollowing),
    # path('api/
    # block_users/', views.block_users),
]