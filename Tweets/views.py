from datetime import datetime
from TUsers.models import TUser
from TUsers.views import is_autherized
from Tweets.models import TCtweets
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Tweets.serializer import TCtweetsSerializer,TCValidator,ReplyValidator,RetweetValidator
from django.core.paginator import Paginator
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

def get_user_obj(user=None):
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
        if is_autherized(request,username):
            validate = TCValidator(request.query_params,request.FILES)
            if not validate.is_valid():
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Invalid username or tweet_text"}
                logger.error(error)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

            try:
                user = get_user_obj(username)
                new_tweet = TCtweets(username=user,tweet_text=text)
                new_tweet.save()
                serializer = TCtweetsSerializer(new_tweet)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "User Does not exist"}
                logger.error(e)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['GET'])
def Timeline(request,username):
    '''
    Purpose: Returns the Timeline of the User in a Paginated Fashion
    Input: page (mandatory) <int>  
    Output: Tweet object with all the tweets in the page
    '''
    if is_autherized(request,username):
        try:
            page_no = int(request.query_params.get('page',1))
            userObj = get_user_obj(username)
            if page_no < 1:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Please pass an integer value (starting with 1) as Page Number"}
                logger.error(error)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
            
            tweets = TCtweets.objects.filter(username=userObj)
            paginator = Paginator(tweets,5) #shows 5 tweets per page
            page_num = paginator.get_page(page_no)
            tweet_objs = page_num.object_list 
            serializer = TCtweetsSerializer(tweet_objs,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "No Tweets to show"}
            logger.error(e)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['DELETE'])
def DeleteTweet(request,tweet_id=None):
    '''
    Purpose: Deletes the tweet having the id in the URL
    Input: None  
    Output: Tweet object that was deleted
    '''
    try:
        tweet = TCtweets.objects.get(id=tweet_id)
        username = tweet.username.username
        if is_autherized(request,username):
            serializer = TCtweetsSerializer(tweet)
            tweet.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)       
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This tweet no longer exists"}
        logger.error(e)    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)     

@api_view(['GET'])
def ShowTweet(request,tweet_id=None):
    '''
    Purpose: displays the tweet with the id in the URL and its replies
    Input: None  
    Output: Tweets and its replies
    '''
    try:
        tweet = TCtweets.objects.filter(id=tweet_id)
        username = tweet.username.username
        if is_autherized(request,username):
            replies = TCtweets.objects.get(id=tweet_id).reply.all()
            tweetNreply = tweet.union(replies)
            serializer = TCtweetsSerializer(tweetNreply,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(e)
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This tweet no longer exists"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def Reply(request,tweet_id=None):
    '''
    Purpose: Reply to the tweet with the id in the URL
    Input: username (mandatory) <str> Account user
           reply_text (mandatory) <str> Reply  
    Output: Replied tweet object
    '''
    try:
        user = request.query_params.get('username',None)
        reply = request.query_params.get('reply_text',None)
        validate = ReplyValidator(request.query_params,request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid username or reply_text"}
            logger.error(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        if is_autherized(request,user):
            user =get_user_obj(user)
            reply_tweet = TCtweets(username=user,tweet_text=reply)
            reply_tweet.save()
            tweet = TCtweets.objects.get(id=tweet_id)
            tweet.reply.add(reply_tweet)
            tweet.save()
            serializer = TCtweetsSerializer(reply_tweet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Error saving the reply"}
        logger.error(e)                    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
def Retweet(request,tweet_id=None):
    '''
    Purpose: Retweet the tweet with the id in the URL
    Input: username (mandatory) <str> Account user
           comment (optional) <str> Comment  
    Output: tweet object with comment
    '''
    try:
        user = request.query_params.get('username',None)
        comment = request.query_params.get('comment',None)
        validate = RetweetValidator(request.query_params,request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid username"}
            logger.error(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        if is_autherized(request,user):
            tweet_text = TCtweets.objects.get(id=tweet_id).tweet_text
            reply_tweet = TCtweets(username = get_user_obj(user),tweet_text=tweet_text,comment=comment)
            reply_tweet.save()
            tweet= TCtweets.objects.get(id=tweet_id)
            tweet.retweet.add(get_user_obj(user))
            tweet.save()
            serializer = TCtweetsSerializer(reply_tweet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Error retweeting!"}
        logger.error(e)                    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
def Like(request,tweet_id=None):
    '''
    Purpose: Like the tweet with the id in the URL
    Input: username (mandatory) <str> Account user 
    Output: tweet object that was liked
    '''
    try:
        user = request.query_params.get('username',None)
        validate = RetweetValidator(request.query_params,request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid username"}
            logger.error(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        if is_autherized(request,user):
            tweet = TCtweets.objects.get(id=tweet_id)
            tweet.like.add(get_user_obj(user))
            tweet.save()
            serializer = TCtweetsSerializer(tweet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Error liking the tweet!"}
        logger.error(e)                    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def Search(request):
    '''
    Search for a tweet using a hashtag and a region
    Input:
    username <str> (mandatory) Account User
    hashtag <str> (mandatory) text (with hashtag) to search with
    '''
    user = request.query_params.get('username')
    hashtag = request.query_params.get('hashtag')
    if is_autherized(request,user):
        try:
            tweet_match = TCtweets.objects.filter(tweet_text__contains=hashtag[1:])
            if tweet_match:
                serializer = TCtweetsSerializer(tweet_match,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                message = {"Message": "No Match found!"}
                return Response(message,status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = {'Error_code': status.HTTP_204_NO_CONTENT,
                            'Error_Message': "Please enter a valid search string"}
            logger.error(e)
        return Response(error, status=status.HTTP_204_NO_CONTENT)
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_tweets(request):
    '''
    Debugging
    '''
    tweets = TCtweets.objects.all()
    serializer = TCtweetsSerializer(tweets,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)