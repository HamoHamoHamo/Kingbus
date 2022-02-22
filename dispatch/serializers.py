import dispatch
from .models import Dispatch, Dispatch_order, User
from rest_framework import serializers

class DispatchOrderSerializer(serializers.ModelSerializer):
    #왕복(lt), 편도(st), 셔틀(ro)?
    # way = serializers.CharField(max_length=2)
    # purpose = serializers.CharField(max_length=100)
    # reference = serializers.CharField(required=False)
    # departure = serializers.CharField(max_length=255)
    # arrival = serializers.CharField(max_length=255)
    # stopover = serializers.CharField(required=False)
    # departure_date = serializers.DateField()
    # departure_time = serializers.TimeField()
    # arrival_date = serializers.DateField(required=False)
    # arrival_time = serializers.TimeField(required=False)
    # is_driver = serializers.BooleanField(default=False)
    # total_number = serializers.CharField(max_length=10)
    # convenience = serializers.CharField(required=False)
    class Meta:
        model = Dispatch_order
        fields = '__all__'

    # get id(pk) of User from token payload
    user_id = serializers.CharField()
    
    def validate(self, attrs):
        return super().validate(attrs)
    def create(self, validated_data):
        user_id=validated_data['user_id']
        del validated_data['user_id']
        orders = Dispatch_order.objects.create(**validated_data)
        dispatch = Dispatch.objects.create(
            order = orders,
            user = User.objects.get(id=user_id)
        )
        return orders, dispatch
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)