# from django.contrib.auth import authenticate
from datetime import datetime

from user.serializers import CompanyDetailSerializer, DriverDetailSerializer
from .models import Dispatch, DispatchEstimate, DispatchOrder#, User
from rest_framework import serializers

class DispatchOrderSerializer(serializers.ModelSerializer):
    #왕복(lt), 편도(st), 셔틀(ro)?
    class Meta:
        model = DispatchOrder
        fields = '__all__'

    # get id(pk) of User from token payload?
    # username = serializers.CharField()
    def get_time_diff(self, attrs, array): #https://stackoverflow.com/questions/9578906/easiest-way-to-combine-date-and-time-strings-to-single-datetime-object-using-pyt
        return datetime.combine(datetime.strptime(str(attrs[array+'_date']), '%Y-%m-%d'), datetime.strptime(str(attrs[array+'_time']), '%H:%M:%S').time())


    def validate(self, attrs):
        if attrs['way'] != 'st' and attrs['way'] != 'lt' and attrs['way'] != 'ro': # 종류3개중 어느것도 아닐때
            raise serializers.ValidationError("Bad Request.1")
        if attrs['way'] != 'st': #편도가 아니면서
            if not 'comeback_date' in attrs or not 'comeback_time' in attrs: #복귀날짜/시간이 없을떄
                raise serializers.ValidationError("Bad Request.2")
            if self.get_time_diff(attrs, 'comeback') < self.get_time_diff(attrs, 'departure'): #복귀날짜가 출발날짜보다 빠를떄
                raise serializers.ValidationError("Bad Request.3")
        elif 'comeback__date' in attrs or 'comeback_time' in attrs: #편도인데 복귀날짜/시간이 있을떄
            raise serializers.ValidationError("Bad Request.4")
        return attrs
    def create(self, validated_data):
        user=self.context['requestuser']
        # TODO naver api 받아서
        orders = DispatchOrder.objects.create(**validated_data, total_distance="1000")  # total_distance여기 넣으면 됨
        Dispatch.objects.create(order=orders,user=user,dispatch_status='1')
        return orders
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    
class DispatchEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchEstimate
        fields = '__all__'
        #exclude = ['driverorcompany']
    # order = serializers.CharField(required=False)

    # price = serializers.CharField(max_length=10)
    # bus_cnt = serializers.CharField(max_length=5)
    # bus_type = serializers.CharField(max_length=64)

    # is_tollgate = serializers.BooleanField(default=False)
    # is_parking = serializers.BooleanField(default=False)
    # is_accomodation = serializers.BooleanField(default=False)
    # is_meal = serializers.BooleanField(default=False)
    # is_convenience = serializers.BooleanField(default=False)

    def validate(self, attrs):
        return super().validate(attrs)
    def create(self, validated_data):
        # validated_data['order'] = DispatchOrder.objects.get(id=validated_data['order'].id)
        # validated_data['driverorcompany'] = self.context['requestuser']
        estimate = DispatchEstimate.objects.create(**validated_data)
        return estimate
    def update(self, instance, validated_data):
        validated_data['order'] = instance.order
        validated_data['driverorcompany'] = instance.driverorcompany
        estimate = DispatchEstimate.objects.update(**validated_data)
        return estimate


class DispatchEstimateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchEstimate
        fields = '__all__'
    dispatch_status = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    driverorcompany_profile = serializers.SerializerMethodField()
    def get_name(self, obj):
        name = obj.driverorcompany.name
        return name
    def get_order(self, obj):
        order = obj.order
        return DispatchOrderSerializer(instance=order).data
    def get_dispatch_status(self, obj):
        dispatch_status = obj.order.dispatch.dispatch_status
        return dispatch_status
    def get_driverorcompany_profile(self, obj):
        try:
            driverorcompany_profile = obj.driverorcompany.driveracc
            return DriverDetailSerializer(driverorcompany_profile).data
        except:
            driverorcompany_profile = obj.driverorcompany.companyacc
            return CompanyDetailSerializer(driverorcompany_profile).data

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)


class DispatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = '__all__'
    orders = serializers.SerializerMethodField()
    def get_orders(self, obj):
        order = obj.order
        return DispatchOrderSerializer(instance=order).data
    
