from dataclasses import field
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'password', 'email', 'name')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_date):
        user = User.objects.create_user(
            userid=validated_date['userid'],
            email=validated_date['email'],
            password=validated_date['password'],
            name=validated_date['name'],
        )
        return user


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAcc
        fields = '__all__'
        # fields = ('userid', 'password', 'email', 'name')
        extra_kwargs = {"password": {"write_only": True}}