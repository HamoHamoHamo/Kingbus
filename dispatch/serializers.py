# from django.contrib.auth import authenticate
from .models import Dispatch, DispatchEstimate, DispatchOrder#, User
from rest_framework import serializers

class DispatchOrderSerializer(serializers.ModelSerializer):
    #왕복(lt), 편도(st), 셔틀(ro)?
    class Meta:
        model = DispatchOrder
        fields = '__all__'

    # get id(pk) of User from token payload?
    # username = serializers.CharField()

    def validate(self, attrs):
        return super().validate(attrs)
    def create(self, validated_data):
        user=self.context['requestuser']
        orders = DispatchOrder.objects.create(**validated_data)
        dispatch = Dispatch.objects.create(
            order = orders,
            user = user
        )
        return orders, dispatch
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


# class DispatchOrderDetailSerializer(serializers.Serializer):

    
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


class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)