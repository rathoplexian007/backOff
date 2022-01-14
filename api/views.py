import email
import imp
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
# Create your views here.
import json

from .models import User

def main(request):
    return HttpResponse('Hello')

class RegisterUser(APIView):
    serializer_class=UserSerializer
    def post(self, request):
        data={
            'email':request.data['email'],
            'password':request.data['password']
        }
        print(data)
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            print('valid')
            serializer.save()
        else:
            print('invalid')
        return Response({},status=status.HTTP_200_OK)

class LoginUser(APIView):
    serializer_class=UserSerializer
    def post(self, request):
        data={
            'email':request.data['email'],
            'password':request.data['password']
        }
        print(data)
        try:
            queryset=User.objects.get(email=data['email'])
            serializer=self.serializer_class(queryset)
            print(serializer.data)
            if serializer.data['password'] == data['password']:
                return Response({'response':True}, status=status.HTTP_200_OK)
            else:
                return Response({'response':False}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response({'response':False}, status=status.HTTP_204_NO_CONTENT)
        
class UploadDocuments(APIView):
    def post(self, request):
        print(request.data)
        data=request.data;
        print(data.get('aadhar'))
        return Response({}, status=status.HTTP_200_OK)

class UserDataView(generics.ListCreateAPIView):
    queryset=User.objects.order_by('email').all()
    serializer_class=UserSerializer