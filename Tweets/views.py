from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
from TUsers.models import TUser
from Tweets.models import TCtweets
from django.http import HttpResponse,QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Tweets.serializer import TCtweetsSerializer,TCValidator
from django.core.paginator import Paginator
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

def get_user_obj(user):
    #Returns User Objects corresponding to the username
    return TUser.objects.get(username=user)

@api_view(['POST'])
def CreateTweet(request):
    '''
    Purpose: Creates a new Tweet
    Input: 
    username: (mandatory) <str> Account user
    tweet_text: (mandatory) <str> Tweet
    Output: TCtweet Object of the created tweet
    '''

    if request.method == "POST":
        username = request.query_params.get('username')
        text = request.query_params.get('tweet_text')
        validate = TCValidator(request.query_params,request.FILES)

        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid username or tweet_text"}
            logger.warning(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_obj(username)
            new_tweet = TCtweets(username=user,tweet_text=text)
            new_tweet.save()
            serializer = TCtweetsSerializer(new_tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User Does not exist"}
            logger.warning(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Timeline(request,username):
    '''
    Purpose: Returns the Timeline of the User in a Paginated Fashion
    Input: page (mandatory) <int>  
    Output: Tweet object with all the tweets in the page
    '''

    try:
        page_no = int(request.query_params.get('page',1))
        userObj = get_user_obj(username)
        if page_no < 1:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Please pass an integer value (starting with 1) as Page Number"}
            logger.warning(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        
        tweets = TCtweets.objects.filter(username=userObj)
        logger.warning(tweets)
        paginator = Paginator(tweets,10) #shows 10 tweets per page
        page_num = paginator.get_page(page_no)
        tweet_objs = page_num.object_list 
        serializer = TCtweetsSerializer(tweet_objs,many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "No Tweets to show"}
        logger.warning(e)                    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 

@api_view(['DELETE'])
def DeleteTweet(request,tweet_id):
    '''
    Purpose: Deletes the tweet having the id in the URL
    Input: None  
    Output: Tweet object that was deleted
    '''
    try:
        tweet = TCtweets.objects.get(id=tweet_id)
        serializer = TCtweetsSerializer(tweet)
        tweet.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This tweet no longer exists"}
        logger.warning(e)    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def ShowTweet(request,tweet_id):
    try:
        print(tweet_id)
        tweet = TCtweets.objects.filter(id=tweet_id)
        print(tweet)
        replies = TCtweets.objects.get(id=tweet_id).reply.all()
        tweetNreply = tweet.union(replies)
        serializer = TCtweetsSerializer(tweetNreply,many=True)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response("Error retreiving the tweet: "+str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def Reply(request,tweet_id):
    try:
        user = request.query_params.get('username')
        reply = request.query_params.get('reply')
        reply_tweet = TCtweets()
        reply_tweet.username = get_user_obj(user)
        reply_tweet.tweet_text = reply
        reply_tweet.save()
        tweet = TCtweets.objects.get(id=tweet_id)
        tweet.reply.add(reply_tweet)
        tweet.save()
        return Response("Reply Saved", status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response("An Error occured: "+str(e), status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def Retweet(request,tweet_id):
    try:
        user = request.query_params.get('username')
        comment = request.query_params.get('comment')
        reply_tweet = TCtweets()
        reply_tweet.username = get_user_obj(user)
        reply_tweet.tweet_text = TCtweets.objects.get(id=tweet_id).tweet_text
        reply_tweet.comment = comment
        reply_tweet.save()
        return Response("Retweet-ed", status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response("An Error occured: "+str(e), status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def Like(request,tweet_id):
    try:
        tweet = TCtweets.objects.get(id=tweet_id)
        # first_like = 1
        tweet.like = tweet.like+1 if tweet.like != None else 1
        tweet.save()
        return Response("Liked!", status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response("Error: "+str(e), status=status.HTTP_400_BAD_REQUEST) 



    
