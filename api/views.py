from email import message
from time import sleep, time
from turtle import pos
import dateutil.parser
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from channels.generic.websocket import AsyncWebsocketConsumer

# Create your views here.
from web3 import Web3
import json
import random
from datetime import datetime, timedelta

from .models import User

def main(request):
    # url='https://rinkeby.infura.io/v3/b28580157fa843e486d1845a0653f9f4';
    # w3=Web3(Web3.HTTPProvider(url))
    # if w3.isConnected():
    #     print('print')
    #     return HttpResponse(w3.eth.blockNumber)
    queryset=Officials.objects.order_by('available_time').all()
    serializer=OfficialsSerializer(queryset[0])
    officialGmail=serializer.data['official_gmail']
    dt=serializer.data['available_time']
    officialGmail='joysen833@gmail.com'
    newdt=dateutil.parser.isoparse(dt)
    newdt+=timedelta(minutes=40)
    
    # update date to extra 40 min
    '''
    queryset=Officials.objects.get(id=serializer.data['id'])
    queryset.available_time=newdt
    queryset.save(update_fields=['available_time'])
    '''
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
    serializer_class=User
    def post(self, request):
        id=request.data.get('blockchain_address');
        try:
            queryset=User.objects.get(blockchain_address=id)
            print(queryset)
            print('user already registered')
        except:
            userserializer=UserSerializer(data=request.data)
            if userserializer.is_valid():
                print('valid data')
                print(userserializer)
                userserializer.save()
            else:
                print('invalid data')
            print('user not registered')
        
        return Response({}, status=status.HTTP_200_OK)

class UserDataView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class OfficalsView(generics.ListCreateAPIView):
    queryset=Officials.objects.order_by('available_time').all()
    serializer_class=OfficialsSerializer

class MeetingView(generics.ListCreateAPIView):
    queryset=Meeting.objects.all()
    serializer_class=MeetingSerializer

class VideoConferenceView(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name='testRoom'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        order_data_json =json.loads(text_data)
        message=order_data_json['message']
        action=order_data_json['action']
        print('recieved dictionary meant to be sent',message)
        if action=='new-offer' or action=='new-answer':
            recieved_channel_name=order_data_json['message']['receiver_channel_name']
            order_data_json['message']['receiver_channel_name']=self.channel_name
            await self.channel_layer.send(recieved_channel_name,{'type':'send.sdp', 'received_dict':order_data_json})         
            return

        recieved_dict=json.loads(text_data)
        recieved_dict['message']['receiver_channel_name']=self.channel_name
        
        await self.channel_layer.group_send(self.room_group_name,{'type':'send.sdp', 'received_dict':recieved_dict})

    async def send_sdp(self, event):
        received_dict=event['received_dict']
        print(event,'group forwarding')
        await self.send(text_data=json.dumps(received_dict))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print('disconneded')

class UnappointedView(APIView):
    def post(self, request):
        print(request.data)
        timestamp1=datetime.now()
        sleep(1)
        timestamp2=datetime.now()
        print(timestamp2>timestamp1)
        # return Response({'response':True}, status=status.HTTP_200_OK)
        try:
            official=OfficialsSerializer(Officials.objects.get(official_account=request.data.get('official'))).data
            idOfOfficial=official['id']
            print('the official is',official)
            idToExclude=[]
            querysetalreadyappointed=Meeting.objects.all()
            for query in querysetalreadyappointed:
                serializer=MeetingSerializer(query)
                idToExclude.append(serializer.data['user'])
            print('excluded ids',idToExclude)
            queryset=User.objects.filter(official_appointed=False).exclude(id__in=idToExclude)
            if not queryset.exists():
                return Response({'response':False}, status=status.HTTP_200_OK)
            
            selectedUser=random.randint(0,len(queryset)-1)
            serializer=UserSerializer(queryset[selectedUser])
            randomUser=serializer.data
            print(official['available_time'])
            randomUser['onTime']=official['available_time']
            return Response(randomUser, status=status.HTTP_200_OK)

            # random user has been selected
        except:
            print('discrded')
            pass
        return Response({'response':True}, status=status.HTTP_200_OK)

class RequestMeeting(APIView):
    def post(self, request):
        try:
            querysetofficials=Officials.objects.filter(official_account=request.data.get('official'))
            querysetuser=User.objects.filter(blockchain_address=request.data.get('randomUser'))
            if querysetofficials.exists() and querysetuser.exists():
                serializerofficials=OfficialsSerializer(querysetofficials[0])
                serializerusers=UserSerializer(querysetuser[0])
                official=serializerofficials.data
                user=serializerusers.data
                print(official,user)
                queryset=Meeting.objects.filter(official=official['id'],meetingTime__gt=official['available_time'])
                print(queryset)
                meet={
                    'user':user['id'],
                    'official':official['id'],
                    'meetlink':request.data.get('meetLink'),
                    'meetingTime':official['available_time']
                }
                serializermeeting=MeetingSerializer(data=meet)
                
                if serializermeeting.is_valid():
                    if queryset.exists():
                        print(queryset)
                        newdt=dateutil.parser.isoparse(official['available_time'])
                        i=0
                        done=False
                        querysetnewoffice=Officials.objects.get(id=official['id'])
                        for i in range(len(queryset)):
                            newdt+=timedelta(minutes=60)
                            serializerregmeeting=MeetingSerializer(queryset[i])
                            regnewdt=dateutil.parser.isoparse(serializerregmeeting.data['meetingTime'])
                            if newdt<regnewdt:
                                querysetnewoffice.available_time=newdt
                                done=True
                                break
                            else:
                                print(newdt,regnewdt,newdt<regnewdt)
                                i+=1
                        if not done:
                            newdt+=timedelta(minutes=60)
                            querysetnewoffice.available_time=newdt
                            pass
                        
                        serializermeeting.save()
                        querysetnewoffice.save(update_fields=['available_time'])
                        # some meeting before this
                    else:
                        newdt=dateutil.parser.isoparse(official['available_time'])
                        print('last date',newdt)
                        newdt+=timedelta(minutes=60)
                        querysetnewoffice=Officials.objects.get(id=official['id'])
                        querysetnewoffice.available_time=newdt
                        serializermeeting.save()
                        querysetnewoffice.save(update_fields=['available_time'])
                        pass
                    pass
                else:
                    return Response({'response':False}, status=status.HTTP_200_OK)

            else:
                return Response({'response':False}, status=status.HTTP_200_OK)
        except:
            return Response({'response':False}, status=status.HTTP_200_OK)
        return Response({'response':True}, status=status.HTTP_200_OK)

class UpdateOfficial(generics.RetrieveUpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class DeleteMeetings(generics.DestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class ShowMeetings(APIView):
    def post(self, request):
        try:
            queryset=User.objects.get(blockchain_address=request.data.get('user'))
            serializeruser=UserSerializer(queryset)
            user=serializeruser.data
            queryset=Meeting.objects.filter(user=user['id'])
            if queryset.exists():
                meet=MeetingSerializer(queryset[0]).data
                meet=dict(meet)
                print(type(meet))
                res={'response':True,'meet':meet}
                # remove unnecessary paameteres
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response({'response':False}, status=status.HTTP_200_OK)
            print(user)
        except:
            pass
        return Response({'response':False}, status=status.HTTP_200_OK)

class ApproveMeeting(APIView):
    def post(self, request):
        try:
            print(request.data)
            querysetuser=User.objects.get(blockchain_address=request.data.get('user'))
            user=UserSerializer(querysetuser).data
            querysetmeeting=Meeting.objects.get(user=user['id'])
            querysetuser.official_appointed=True
            querysetmeeting.pending=False
            querysetmeeting.save(update_fields=['pending'])
            querysetuser.save(update_fields=['official_appointed'])
            meeting=MeetingSerializer(querysetmeeting).data
            official_address=OfficialsSerializer(Officials.objects.get(id=meeting['official'])).data['official_account']
            print(user,meeting)
            return Response({'response':True,'official_address':official_address }, status=status.HTTP_200_OK)
        except:
            pass
        return Response({'response':False}, status=status.HTTP_200_OK)

class DeleteMeeting(APIView):
    def post(self, request):
        try:
            print(request.data)
            querysetuser=User.objects.get(blockchain_address=request.data.get('user'))
            user=UserSerializer(querysetuser).data
            querysetmeeting=Meeting.objects.get(user=user['id'])
            querysetmeeting.delete()
            return Response({'response':True}, status=status.HTTP_200_OK)
        except:
            pass
        return Response({'response':False}, status=status.HTTP_200_OK)

class ShowAllMeetingsForAdmin(APIView):
    def post(self, request):
        try:
            print(request.data)
            querysetofficial=Officials.objects.get(official_account=request.data.get('official'))
            official=OfficialsSerializer(querysetofficial).data
            querysetmeetings=Meeting.objects.filter(official=official['id'])
            allMeetings=[]
            for query in querysetmeetings:
                serializers=MeetingSerializer(query)
                meet=serializers.data
                meet['user_blockchain_address']=UserSerializer(User.objects.get(id=meet['user'])).data['blockchain_address']
                meet['official_blockchain_address']=OfficialsSerializer(Officials.objects.get(id=meet['official'])).data['official_account']
                print(meet,type(meet))
                allMeetings.append(meet)
            return Response({'response':True, 'meetings':allMeetings}, status=status.HTTP_200_OK)            
        except:
            pass
        return Response({'response':False}, status=status.HTTP_200_OK)

