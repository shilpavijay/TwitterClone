from django.shortcuts import render
from TUsers.models import TUser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from TUsers.serializer import TUserSerializer
import json
import logging
import datetime
from django.conf import settings
import jwt

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,)

EXP_TIME = datetime.timedelta(hours=1)

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

def GetToken(username):
    '''
    Purpose: Get Access token
    Input: 
    username (mandatory) <str> Account user 
    password (mandatory) <str> Password
    Output: Token that expires in 60 minutes
    '''
    try:
        user = TUser.objects.get(username=username)
        if user:
            try:
                payload = {'id':user.id,'username':user.username,'exp':datetime.datetime.utcnow()+EXP_TIME}
                token = {'token':jwt.encode(payload,settings.AUTH_TOKEN).decode('utf8')}
                                # jwt.encode({'exp': datetime.utcnow()}, 'secret')
                return token
            except Exception as e:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Error generating Auth Token"}
                logger.error(e)
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username or Password"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
def Login(request,username=None,password=None):
    '''
    Authenticate if username and password is correct. 
    Input
    Output: return User object or Error 
    '''
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    try:
        user = TUser.objects.get(username=username)
        if user.password == password:
            token = GetToken(username)
            user.token = token['token']
            user.save()
            request.session['authtoken'] = token
            serializer = TUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username or Password"}
            return Response(error,status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username"}
        logger.error(e) 
        return Response(error,status=status.HTTP_400_BAD_REQUEST)         

def Auth(request,username):
    '''
    Purpose: Login to the Application
    Input: 
    token (mandatory) <str> user token 
    Output: User object of the logged in user
    '''
    try:
        token = request.session.get('authtoken').get('token')
        payload = jwt.decode(token,settings.AUTH_TOKEN)
        user = TUser.objects.get(username=username)
        if payload.get('username') == user.username:
            serializer = TUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Invalid User"}
            logger.error(error)
            return Response(error,status=status.HTTP_403_FORBIDDEN) 
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Token is Invalid/Expired"}
        logger.error(e)
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
    except Exception as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
 
def is_autherized(request,username):
    validation = Auth(request,username)
    if validation.status_code == 200:
        return True
    else:
        return False


@api_view(['PUT'])
def AccountUpdate(request,username):
    '''
    Purpose: Update Account Details
    Input: 
    username (mandatory) <str> Chosen Username 
    country (optional) <str> Country
    Output: User object of the updated user
    '''
    if is_autherized(request,username):
        try:
            country = request.query_params.get('country')
            user = TUser.objects.get(username=username)
            user.country = country
            user.save()
            serializer = TUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Invalid details"}
            logger.error("AccountUpdate: Error: "+str(e))
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def FollowUser(request,loggedin_user,user):
    '''
    Purpose: Follow the user
    Input: -
    Output: User object of the logged in user
    '''
    if is_autherized(request,loggedin_user):
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
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetFollowers(request,username):
    '''
    Purpose: Get all the followers for the user
    Input: -
    Output: User object of all the following users
    '''
    if is_autherized(request,username):
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
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)            

@api_view(['GET'])
def GetFollowing(request,username):
    '''
    Purpose: Get all the users the given user is following
    Input: -
    Output: User object of all the followed users
    '''
    if is_autherized(request,username):
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
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def Block_user(request,username):
    '''
    Purpose: Block the user
    Input: -
    Output: Blocked user
    '''
    if is_autherized(request,username):
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
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
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