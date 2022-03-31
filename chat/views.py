import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Message, ChatroomList
from .serializers import ChatSerializer, UserChatroomListSerializer, DriverOrCompanyChatroomListSerializer


@api_view(('GET',))
def room(request, room_pk):
    # username = request.GET.get('username')#,'Anonymous'
    # chatroom = ChatroomList.objects.get(pk=room_pk)
    chatroom = get_object_or_404(ChatroomList, pk=room_pk)
    messages = Message.objects.filter(room=chatroom.chatroom)#[0:25]
    # 방 이름 토큰으로생성, 생성한 토큰은 유저모델에 채팅방 목록 칼럼 개설후 거기에 저장
    return Response(ChatSerializer(messages, many=True).data)
    #request,'chat/room.html',{'room_name':room_name, 'username':username, 'messages':messages}


@api_view(('GET',))
def chatroomlist(request):
    if request.user.role == 'u':
        chatroomlist = ChatroomList.objects.filter(user=request.user).select_related('driverorcompany')
        if not chatroomlist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(DriverOrCompanyChatroomListSerializer(chatroomlist, many=True).data)
    elif request.user.role == 'd' or request.user.role == 'c':
        chatroomlist = ChatroomList.objects.filter(driverorcompany=request.user).select_related('user')
        if not chatroomlist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(UserChatroomListSerializer(chatroomlist, many=True).data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def createchatroom(request):
    print(request)
    requestuser = request.user
    if requestuser.role == 'u':
        if not 'driverorcompany' in request.data or 'user' in request.data:
            print('1')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            print('2')
            chatroom = ChatroomList.objects.get(user=requestuser, driverorcompany__id=request.data['driverorcompany'])
            print('3')
            return Response({'detail':'chat already exists', 'location':chatroom.chatroom}, status=status.HTTP_301_MOVED_PERMANENTLY)
        except ObjectDoesNotExist:
            chatroom = ChatroomList.objects.create(user=requestuser, driverorcompany__id=request.data['driverorcompany'], chatroom=uuid.uuid4())
            return Response({'detail':'chat created', 'location':chatroom.chatroom}, status=status.HTTP_201_CREATED)
        
        
    elif requestuser.role == 'd' or requestuser.role == 'c':
        if not 'user' in request.data or 'driverorcompany' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            chatroom = ChatroomList.objects.get(user__id=request.data['user'], driverorcompany=requestuser)
            return Response({'detail':'chat already exists', 'location':chatroom.chatroom}, status=status.HTTP_301_MOVED_PERMANENTLY)
        except ObjectDoesNotExist:
            chatroom = ChatroomList.objects.create(user__id=request.data['user'], driverorcompany=requestuser, chatroom=uuid.uuid4())
            return Response({'detail':'chat created', 'location':chatroom.chatroom}, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)