# from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# from django.conf import settings
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
        # user = authenticate(**data)
        # if user is None:
        except:
            raise serializers.ValidationError("Invalid ID")
        # if data['role'] is None:
        #     raise serializers.ValidationError("Invalid login credentials2")
        # if len(data['role'])>1:
        #     raise serializers.ValidationError("Bad Request")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")
        if data['role']!=user.role:
            raise serializers.ValidationError("Invalid login credentials")
        # TODO https://eunjin3786.tistory.com/271
    
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        # refresh['id'] = user.id
        access_token = str(refresh.access_token)
        

        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': user.username,
            'name': user.name,
            'role' : user.role
        }
        return validation

'''
class DriverLoginSerializer(serializers.Serializer):

class CompanyLoginSerializer(serializers.Serializer):
'''

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name' , 'num')
        extra_kwargs = {"password": {"write_only": True}}
    def validate(self, data):# TODO merge functions
        if len(str(data['username'])) < 4:
            raise serializers.ValidationError("ID가 너무 짧습니다.")
        if len(str(data['password'])) < 4:
            raise serializers.ValidationError("비밀번호가 너무 짧습니다.")
        if len(str(data['num'])) < 10:
            raise serializers.ValidationError("전화번호가 너무 짧습니다.")
        return data
    def create(self, validated_data):
        validated_data['role']='u'
        validated_data['is_active']=True
        user = User.objects.create_user(**validated_data)
        return user


class DriverRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name' , 'num', 'driver_com_name', 'driver_car_driverlicense')
        extra_kwargs = {"password": {"write_only": True}}
    driver_com_name = serializers.CharField(max_length=32)
    driver_car_driverlicense = serializers.ImageField()
    def validate(self, data):
        if len(str(data['username'])) < 4:
            raise serializers.ValidationError("ID가 너무 짧습니다.")
        if len(str(data['password'])) < 4:
            raise serializers.ValidationError("비밀번호가 너무 짧습니다.")
        if len(str(data['num'])) < 10:
            raise serializers.ValidationError("전화번호가 너무 짧습니다.")
        return data
    def create(self, validated_data):
        validated_data['role']='d'
        driver_com_name = validated_data.pop('driver_com_name')
        driver_car_driverlicense = validated_data.pop('driver_car_driverlicense')
        user = User.objects.create_user(**validated_data)
        driver = DriverAcc.objects.create(
            user = user,
            driver_com_name=driver_com_name,
            driver_car_driverlicense=driver_car_driverlicense,
        )
        return user, driver


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name' , 'num', 'company_com_name', 'company_business_registration')
        extra_kwargs = {"password": {"write_only": True}}
    company_com_name = serializers.CharField(max_length=32)
    company_business_registration = serializers.ImageField()
    def validate(self, data):
        if len(str(data['username'])) < 4:
            raise serializers.ValidationError("ID가 너무 짧습니다.")
        if len(str(data['password'])) < 4:
            raise serializers.ValidationError("비밀번호가 너무 짧습니다.")
        if len(str(data['num'])) < 10:
            raise serializers.ValidationError("전화번호가 너무 짧습니다.")
        return data
    def create(self, validated_data):
        validated_data['role']='c'
        company_com_name = validated_data.pop('company_com_name')
        company_business_registration = validated_data.pop('company_business_registration')
        user = User.objects.create_user(**validated_data)
        company = CompanyAcc.objects.create(
            user = user,
            company_com_name=company_com_name,
            company_business_registration=company_business_registration,
        )
        return user, company


class DriverProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('username', 'password', 'role')
    driver = serializers.SerializerMethodField()
    def get_driver(self, obj):
        instance = obj.driveracc
        return DriverDetailSerializer(instance).data


class CompanyProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('username', 'password', 'role')
    company = serializers.SerializerMethodField()
    def get_company(self, obj):
        instance = obj.companyacc
        return CompanyDetailSerializer(instance).data


class DriverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAcc
        # fields = '__all__'
        exclude = ('user',)
    driver_com_name = serializers.CharField(required=False)
    driver_car_driverlicense = serializers.ImageField(required=False)

    
class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAcc
        # fields = '__all__'
        exclude = ('user',)
    company_com_name = serializers.CharField(required=False)
    company_business_registration = serializers.ImageField(required=False)

