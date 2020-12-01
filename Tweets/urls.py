from django.urls import path
from . import views

urlpatterns = [
    path('tweet', views.CreateTweet), 
    # path('<str: username>', views.Timeline), 
    # path('tweet/<int: tweet_id>/delete', views.DeleteTweet),
    # path('tweet/<int: tweet_id>/', views.ShowTweet), 
    # path('tweet/<int: tweet_id>/reply', views.ReplyTo),
    # path('tweet/<int: tweet_id>/retweet', views.Retweet),
    # path('tweet/<int: tweet_id>/like', views.Like),
    # path('search', views.Search),
]