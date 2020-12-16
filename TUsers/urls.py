from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.AccountSignup),
    path('login', views.Login),
    path('<str:username>/account', views.AccountUpdate),
    path('token', views.GetToken),
    path('auth', views.Auth),
    path('<str:loggedin_user>/<str:user>/follow', views.FollowUser),
    path('<str:username>/followers', views.GetFollowers),
    path('<str:username>/following', views.GetFollowing),
    path('<str:username>/block', views.Block_user), 
    path('users',views.users), #debugging
]