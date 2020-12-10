from django.shortcuts import render
from TUsers.models import TUser
from django.http import HttpResponse,QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from TUsers.serializer import TUserSerializer
import json
import logging
import datetime
from django.conf import settings
import jwt
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,)

EXP_TIME = datetime.timedelta(minutes=5)

def _get_token(request=None):
    return request.META.get('HTTP_AUTHORIZATION') or request.query_params['token']

@api_view(['POST'])
def GetToken(request):
    '''
    Purpose: Get Access token
    Input: 
    username (mandatory) <str> Account user 
    password (mandatory) <str> Password
    Output: Token that expires in 5 minutes
    '''
    user = request.query_params.get('username',None)
    pwd = request.query_params.get('password',None)
    try:
        user = TUser.objects.get(username=user,password=pwd)
        if user:
            try:
                payload = {'id':user.id,'username':user.username,'exp':datetime.datetime.utcnow()+EXP_TIME}
                token = {'token':jwt.encode(payload,settings.AUTH_TOKEN)}
                return Response(token, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            resp = {"Error": 'Authentication Failed. Wrong Username/Password'}
            return Response(resp, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Please provide a valid Username and Password"}
        logger.error(e) 
        return Response(error,status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
def Login(request):
    '''
    Purpose: Login to the Application
    Input: 
    token (mandatory) <str> user token 
    Output: User object of the logged in user
    '''
    token = _get_token(request)
    try:
        payload = jwt.decode(token,settings.AUTH_TOKEN)
        user = TUser.objects.get(username = payload.get('username'))
        serializer = TUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError):
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Token is Invalid"}
        logger.error(e) 
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
    except Exception as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
    
@api_view(['POST'])
def AccountSignup(request):
    '''
    Purpose: Create a new user
    Input: 
    username (mandatory) <str> Chosen Username 
    password (mandatory) <str> Chosen Password
    Output: User object of the created user
    '''
    serializer = TUserSerializer(data=request.query_params)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
def AccountUpdate(request,username):
    '''
    Purpose: Update Account Details
    Input: -
    username (mandatory) <str> Chosen Username 
    country (optional) <str> Country
    Output: User object of the updated user
    '''
    try:
        query_dict = QueryDict('', mutable=True)
        query_dict.update({"username": username})
        query_dict.update(request.query_params)
        serializer = TUserSerializer(data=query_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid details"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def FollowUser(request,loggedin_user,user):
    '''
    Purpose: Follow the user
    Input: -
    Output: User object of the logged in user
    '''
    try:
        cur_user=TUser.objects.get(username=loggedin_user)
        fol_user=TUser.objects.get(username=user)
        cur_user.following.add(fol_user)
        cur_user.save()
        serializer = TUserSerializer(cur_user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Request Failed. Invalid Details"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def GetFollowers(request,username):
    '''
    Purpose: Get all the followers for the user
    Input: -
    Output: User object of all the following users
    '''
    try:
        user = TUser.objects.get(username=username)
        followers = user.followers.all()
        serializer = TUserSerializer(followers, many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def GetFollowing(request,username):
    '''
    Purpose: Get all the users the given user is following
    Input: -
    Output: User object of all the followed users
    '''
    try:
        user = TUser.objects.get(username=username)
        following = user.following.all()
        serializer = TUserSerializer(following, many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
def Block_user(request,username):
    '''
    Purpose: Block the user
    Input: -
    Output: Blocked user
    '''
    try:
        user = TUser.objects.get(username=username)
        user.blocked = True
        user.save()
        serializer = TUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def users(request):
    '''
    Debugging
    '''
    if request.method == 'GET':
        users = TUser.objects.all()
        serializer = TUserSerializer(users, many=True)
        return Response(serializer.data)        