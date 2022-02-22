from distutils.command.config import config
import jwt
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from kingbus.settings import SIMPLE_JWT
from .models import User, DriverAcc, CompanyAcc


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.CharField()
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        # if data['username'].isdigit():
        #     try:user = User.objects.get(num=data['username'])
        #     finally:pass
        # elif '@' in data['username']:
        #     try:user = User.objects.get(email=data['username'])
        #     finally:pass
        # else:
        try:
            user = User.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid login credentials")
        # if data['role'] is None:
        #     raise serializers.ValidationError("Invalid login credentials2")
        if len(data['role'])>1:
            raise serializers.ValidationError("Invalid login credentials3")
        elif data['role']!=user.role:
            raise serializers.ValidationError("Invalid login credentials4")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")

    
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        refresh['id'] = user.id
        access_token = str(refresh.access_token)
        

        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': user.username,
            'role' : user.role
        }
        return validation

'''
class DriverLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            driver = DriverAcc.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid login credentials")
        if not driver.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")
    
        refresh = RefreshToken.for_user(driver)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': driver.username,
        }
        return validation

class CompanyLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            company = CompanyAcc.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid login credentials")
        if not company.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")
    
        refresh = RefreshToken.for_user(company)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': company.username,
        }
        return validation
'''

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name' , 'num')
        extra_kwargs = {"password": {"write_only": True}}
    def validate(self, data):
        if len(str(data['username'])) < 8:
            raise serializers.ValidationError("ID가 너무 짧습니다.")
        if len(str(data['password'])) < 4:
            raise serializers.ValidationError("비밀번호가 너무 짧습니다.")
        if len(str(data['num'])) < 10:
            raise serializers.ValidationError("전화번호가 너무 짧습니다.")
        return data
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            num=validated_data['num'],
            role='u',
            is_active=True,
        )
        return user


class DriverRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=16)
    num = serializers.CharField(max_length=12)
    driver_com_name = serializers.CharField(max_length=32)
    driver_car_driverlisence = serializers.ImageField()
    def validate(self, data):
        if len(str(data['username'])) < 8:
            raise serializers.ValidationError("ID가 너무 짧습니다.")
        if len(str(data['password'])) < 4:
            raise serializers.ValidationError("비밀번호가 너무 짧습니다.")
        if len(str(data['num'])) < 10:
            raise serializers.ValidationError("전화번호가 너무 짧습니다.")
        return data
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            num=validated_data['num'],
            role='d',
        )
        driver = DriverAcc.objects.create(
            user = user,
            driver_com_name=validated_data['driver_com_name'],
            driver_car_driverlisence=validated_data['driver_car_driverlisence'],
        )
        return user, driver


class CompanyRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=16)
    num = serializers.CharField(max_length=12)
    company_com_name = serializers.CharField(max_length=32)
    company_business_registration = serializers.ImageField()
    def validate(self, data):
        if len(str(data['username'])) < 8:
            raise serializers.ValidationError("ID가 너무 짧습니다.")
        if len(str(data['password'])) < 4:
            raise serializers.ValidationError("비밀번호가 너무 짧습니다.")
        if len(str(data['num'])) < 10:
            raise serializers.ValidationError("전화번호가 너무 짧습니다.")
        return data
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            num=validated_data['num'],
            role='c',
        )
        company = CompanyAcc.objects.create(
            user = user,
            company_com_name=validated_data['company_com_name'],
            company_business_registration=validated_data['company_business_registration'],
        )
        return user, company

