from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreateTweet),
    path('<str:username>/', views.Timeline), 
    path('<int:tweet_id>/delete', views.DeleteTweet),
    path('<int:tweet_id>', views.ShowTweet), 
    path('<int:tweet_id>/reply', views.Reply),
    path('<int:tweet_id>/retweet', views.Retweet),
    path('<int:tweet_id>/like', views.Like),
    # path('search', views.Search),
]