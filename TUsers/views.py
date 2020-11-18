from django.shortcuts import render
from django.conf.urls import url
from TUsers.models import TUser
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from TUsers.serializer import TUserSerializer
import json
# from rest_framework.views import viewsets

# class UserAPIView(viewsets.ViewSet):
@api_view(['POST'])
def Landing(request):
    return HttpResponse("Hi there!")

@api_view(['POST'])
def Authenticate(request):
    #Create Auth token and store it
    #Verify with username and password
    return HttpResponse("Auth...")

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
        