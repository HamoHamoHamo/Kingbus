# from django.conf import settings
from multiprocessing import context
from django.core import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# import jwt

from dispatch.models import Dispatch, DispatchEstimate, DispatchOrder
from .serializers import DispatchEstimateSerializer, DispatchOrderSerializer #DispatchOrderDetailSerializer, 


class DispatchOrderView(APIView):
    serializer_class = DispatchOrderSerializer
    # permission_classes = (AllowAny,)

    # def decode_user_id(request):
    #     user_id_decoded = jwt.decode(request.META['HTTP_AUTHORIZATION'].split(' ')[1], SIMPLE_JWT['SIGNING_KEY'], algorithms=["HS256"])['id']
    #     return user_id_decoded
    # == request.auth

    def get(self, request, **kwargs):
        try:
            if not kwargs['user_id'] is request.user.id:
                return Response({"message": "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)
        # dispatch = Dispatch.objects.filter(user=request.user)
        order = DispatchOrder.objects.filter(dispatch__user=request.user)
        return Response(DispatchOrderSerializer(order, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        try:
            if kwargs['user_id']:
                return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)
        except:pass
        serializer = self.serializer_class(data=request.data, context={'requestuser':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'dispatch': serializer.validated_data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


class DispatchOrderDetailView(APIView):
    serializer_class = DispatchOrderSerializer

    def get(self, request, **kwargs):
        try:
            order = DispatchOrder.objects.get(id=kwargs['order_id'])
            # dispatch = Dispatch.objects.get(order=order) same w/ below
            dispatch = Dispatch.objects.get(order__id=kwargs['order_id'])
        except:
            return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)
        if dispatch.user != request.user:
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)
        return Response(self.serializer_class(instance=order).data)

    def put(self, request, **kwargs):
        try:
            order = DispatchOrder.objects.get(id=kwargs['order_id'])
            dispatch = Dispatch.objects.get(order=order)
        except:
            return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=order, data=request.data)
        if dispatch.user != request.user:
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'data': serializer.validated_data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        try:
            order = DispatchOrder.objects.get(id=kwargs['order_id'])
            dispatch = Dispatch.objects.get(order=order)
        except:
            return Response({"message": "Page Not Found."}, status=status.
        HTTP_404_NOT_FOUND)
        if dispatch.user == request.user:
            order.delete()
            return Response({"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)


class DispatchEstimateView(APIView):
    serializer_class = DispatchEstimateSerializer

    # def get(self, request, **kwargs):
    #     try:
    #         if not kwargs['order_id'] is request.user.id:
    #             return Response({"message": "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)
    #     except:
    #         return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)
    #     # dispatch = Dispatch.objects.filter(user=request.user)
    #     order = DispatchOrder.objects.filter(dispatch__user=request.user)
    #     return Response(DispatchOrderSerializer(order, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != 'c' and 'd':
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)
        estimate = None
        try:
            order = DispatchOrder.objects.get(id=request.data['order'])
            estimate = DispatchEstimate.objects.get(order=order, driverorcompany=request.user)
        except:pass
        if estimate:
            return Response({"You can't apply more than 1 offer in same Order!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data, context={'requestuser':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'estimate': serializer.validated_data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)



class DispatchEstimateDetailView(APIView):
    serializer_class = DispatchEstimateSerializer

    def get(self, request, **kwargs):
        try:
            estimate = DispatchEstimate.objects.get(id=kwargs['estimate_id'])
        except:
            return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)
        if estimate.driverorcompany != request.user:
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)
        return Response(self.serializer_class(instance=estimate).data)

    def put(self, request, **kwargs):
        try:
            estimate = DispatchEstimate.objects.get(id=kwargs['estimate_id'])
        except:
            return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=estimate, data=request.data, context={'requestuser':request.user})
        if estimate.driverorcompany != request.user:
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'data': serializer.validated_data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        try:
            estimate = DispatchEstimate.objects.get(id=kwargs['estimate_id'])
        except:
            return Response({"message": "Page Not Found."}, status=status.
        HTTP_404_NOT_FOUND)
        if estimate.driverorcompany == request.user:
            estimate.delete()
            return Response({"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Invalid Credentials."}, status=status.HTTP_403_FORBIDDEN)