from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
from Tweets.models import TCtweets
from django.http import HttpResponse,QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from TUsers.serializer import TUserSerializer

@api_view(['POST'])
def CreateTweet(request):
    pass