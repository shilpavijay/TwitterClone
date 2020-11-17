from django.shortcuts import render
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

def landing(request):
    return HttpResponse("Hi There!!")

# @api_view(['GET'])
# def users(request):
#     if request.method == 'GET':
#         users = Auth.objects.all()
#         serializer = AuthSerializer(users, many=True)
#         return Response(serializer.data)

# @api_view(['GET'])
# def user_details(request, pk):
#     try:
#         user_details = Auth.objects.get(pk=pk)
#     except Auth.DoesNotExist:
#         return HttpResponse(status=404)
        
#     if request.method == 'GET':
#         serializer = AuthSerializer(user_details)
#         return Response(serializer.data)

# @api_view(['POST'])
# def add_user(request):
#     if request.method == 'POST':
#         serializer = AuthSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
