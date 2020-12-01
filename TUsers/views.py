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

EXP_TIME = datetime.timedelta(minutes=5)

def _get_token(request=None):
    return request.META.get('HTTP_AUTHORIZATION') or request.query_params['token']

@api_view(['POST'])
def GetToken(request):
    user = request.query_params['username']
    pwd = request.query_params['password']
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
            resp = {'Authentication Failed. Wrong Username/Password'}
            return Response(resp, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response("Please provide a valid Username and Password",status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
def Login(request):
    token = _get_token(request)
    try:
        payload = jwt.decode(token,settings.AUTH_TOKEN)
        user = TUser.objects.get(username = payload.get('username'))
        serializer = TUserSerializer(user)
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError):
        return Response("Error: Token is Invalid", status=status.HTTP_403_FORBIDDEN)
    except:
        return Response("Error: Internal Server Error", status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def AccountSignup(request):
    serializer = TUserSerializer(data=request.query_params)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = TUser.objects.all()
        serializer = TUserSerializer(users, many=True)
        return Response(serializer.data)
        
@api_view(['PUT'])
def AccountUpdate(request,username):
    try:
        query_dict = QueryDict('', mutable=True)
        query_dict.update({"username": username})
        query_dict.update(request.query_params)
        serializer = TUserSerializer(data=query_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("Invalid details", status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def FollowUser(request,loggedin_user,user):
    try:
        cur_user=TUser.objects.get(username=loggedin_user)
        fol_user=TUser.objects.get(username=user)
        cur_user.following.add(fol_user)
        cur_user.save()
        return Response("Follow Request Updated", status=status.HTTP_204_NO_CONTENT)
    except:
        return Response("Request Failed. Invalid Details", status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
def GetFollowers(request,username):
    try:
        user = TUser.objects.get(username=username)
        followers = user.followers.all()
        serializer = TUserSerializer(followers, many=True)
        return Response(serializer.data)
    except:
        return Response("User does not exist!", status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def GetFollowing(request,username):
    try:
        user = TUser.objects.get(username=username)
        following = user.following.all()
        serializer = TUserSerializer(following, many=True)
        return Response(serializer.data)
    except:
        return Response("User does not exist!", status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def Block_user(request,username):
    try:
        user = TUser.objects.get(username=username)
        user.blocked = True
        user.save()
        return Response("User Blocked", status=status.HTTP_204_NO_CONTENT)
    except:
        return Response("User Does not exist!", status=status.HTTP_400_BAD_REQUEST) 