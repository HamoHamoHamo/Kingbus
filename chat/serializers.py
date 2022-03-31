from rest_framework import serializers
from .models import Message, ChatroomList
from user.models import User


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # fields = '__all__'
        exclude = ['room']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','role']

class UserChatroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatroomList
        # exclude = ['chatroom']
        fields = '__all__'
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        user = obj.user
        return UserSerializer(user).data

class DriverOrCompanyChatroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatroomList
        # exclude = ['chatroom']
        fields = '__all__'
    driverorcompany = serializers.SerializerMethodField()
    def get_driverorcompany(self, obj):
        driverorcompany = obj.driverorcompany
        return UserSerializer(driverorcompany).data
