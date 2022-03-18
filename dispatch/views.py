# from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework.permissions import AllowAny
# import jwt
# from rest_framework.pagination import PageNumberPagination

from dispatch.models import Dispatch, DispatchEstimate, DispatchOrder
from .serializers import DispatchListSerializer, DispatchSerializer, DispatchEstimateSerializer, DispatchOrderSerializer #DispatchOrderDetailSerializer, 

def invalid_credentials():
    return Response({"message": "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)

def page_not_found():
    return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)

class DispatchOrderView(APIView):
    serializer_class = DispatchOrderSerializer
    # permission_classes = (AllowAny,)

    # def decode_user_id(request):
    #     user_id_decoded = jwt.decode(request.META['HTTP_AUTHORIZATION'].split(' ')[1], SIMPLE_JWT['SIGNING_KEY'], algorithms=["HS256"])['id']
    #     return user_id_decoded
    # == request.auth

    def get(self, request, **kwargs):
        if 'user_id' in kwargs:
            if not kwargs['user_id'] is request.user.id:
                return invalid_credentials()
            # dispatch = Dispatch.objects.filter(user=request.user)
            order = DispatchOrder.objects.filter(dispatch__user=request.user)
            if order:
                return Response(self.serializer_class(order, many=True).data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No Contents"}, status=status.HTTP_204_NO_CONTENT)        
        else:
            return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        try:
            if kwargs['user_id']:
                return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)
        except:pass
        if request.user.role != 'u':
            return invalid_credentials() #"detail": "You must be User to apply order!"
        serializer = self.serializer_class(data=request.data, context={'requestuser':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'dispatch': serializer.data
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
            return page_not_found()
        if dispatch.user != request.user:
            return invalid_credentials()
        return Response(self.serializer_class(instance=order).data)

    def put(self, request, **kwargs):
        try:
            order = DispatchOrder.objects.get(id=kwargs['order_id'])
            dispatch = Dispatch.objects.get(order=order)
        except:
            return page_not_found()
        serializer = self.serializer_class(instance=order, data=request.data)
        if dispatch.user != request.user:
            return invalid_credentials()
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
            return page_not_found()
        if dispatch.user == request.user:
            order.delete()
            return Response({"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return invalid_credentials()


class DispatchEstimateView(APIView):
    serializer_class = DispatchEstimateSerializer

    def get(self, request, **kwargs):
        estimate = None
        if 'user_id' in kwargs:
            if request.user.id is kwargs['user_id']:
                estimate = DispatchEstimate.objects.filter(driverorcompany=request.user)
                print(estimate.first())
                if estimate.first().driverorcompany != request.user:
                    return invalid_credentials()
                return Response(self.serializer_class(instance=estimate, many=True).data)
            else:
                return page_not_found()
        elif 'order_id' in kwargs:
            try:
                dispatch = Dispatch.objects.get(order=kwargs['order_id'])
                estimate = DispatchEstimate.objects.filter(order=kwargs['order_id'])
                if estimate:
                # TODO https://docs.djangoproject.com/en/dev/ref/models/querysets/#exists
                    if dispatch.user == request.user:
                        return Response(self.serializer_class(instance=estimate, many=True).data)
                    else:
                        return invalid_credentials()
            except:
                return page_not_found()
        elif not kwargs:
            return Response({"detail": "Method \"GET\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response({"message": "No Contents"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, **kwargs):
        # print(request.user.role)
        if kwargs:
            return Response({"detail": "Method \"POST\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.user.role != 'c' and not 'd':
            return invalid_credentials()
        try:
            order = DispatchOrder.objects.get(id=request.data['order'])
        except:
            return Response({"message": "Bad request", "detail": "Order argument not given or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            estimate = DispatchEstimate.objects.filter(order=order, driverorcompany=request.user)
        except:
            estimate = None
        finally:
            if estimate:
                return Response({"message": "Bad request", "detail": "You can't apply more than 1 offer in same Order!"}, status=status.HTTP_400_BAD_REQUEST)
        requestdata = request.data.copy()
        # requestdata['order']=DispatchOrder.objects.get(id=requestdata['order'])
        requestdata['driverorcompany']=request.user.id
        serializer = self.serializer_class(data=requestdata, context={'requestuser':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'estimate': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


class DispatchEstimateDetailView(APIView):
    serializer_class = DispatchEstimateSerializer

    def get(self, request, **kwargs):
        try:
            if kwargs['estimate_id']:
                estimate = DispatchEstimate.objects.get(id=kwargs['estimate_id'])
        except:
            return page_not_found()
        if estimate.driverorcompany != request.user:
            return invalid_credentials()
        return Response(self.serializer_class(instance=estimate).data)

    def put(self, request, **kwargs):
        try:
            estimate = DispatchEstimate.objects.get(id=kwargs['estimate_id'])
        except:
            return page_not_found()
        if estimate.driverorcompany != request.user:
            return invalid_credentials()
        requestdata = request.data.copy()
        print(estimate.order.id)
        requestdata['order'] = estimate.order.id
        requestdata['driverorcompany'] = request.user.id
        serializer = self.serializer_class(instance=estimate, data=requestdata)# , context={'requestuser':request.user}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'data': self.serializer_class(instance=estimate).data,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        try:
            estimate = DispatchEstimate.objects.get(id=kwargs['estimate_id'])
        except:
            return page_not_found()
        if estimate.driverorcompany == request.user:
            estimate.delete()
            return Response({"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return invalid_credentials()


class DispatchView(APIView):
    serializer_class = DispatchSerializer

    def post(self, request):
        try:
            dispatch = Dispatch.objects.get(order=request.data['order'])
        except:
            return Response({"message": "Bad request", "detail": "Order argument not given or invalid."}, status=status.HTTP_400_BAD_REQUEST)            
        if request.user != dispatch.user or request.user.role != 'u':
            return invalid_credentials()
        if dispatch.reservation_confirmed:
            return Response({"message": "Bad request", "detail": "Reservation already confirmed. Cancel the Order and re-submit."}, status=status.HTTP_400_BAD_REQUEST)
        if not 'selected_estimate' in request.data:
            return Response({"message": "Bad request", "detail": "Estimate argument not given or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            requestdata = request.data.copy()
            requestdata['user']= request.user.id
            # ['estimate_order_time']
            requestdata['estimate_confirmed_time']=timezone.now()
            requestdata['reservation_confirmed']=True
            serializer = self.serializer_class(dispatch, requestdata)
            valid = serializer.is_valid(raise_exception=True)
            # print(serializer.validated_data['selected_estimate'].order)
            # print(dispatch.order)
            if serializer.validated_data['selected_estimate'].order == dispatch.order:
                if valid:
                    serializer.save()
                    response = {
                        'success': True,
                        'statusCode': status.HTTP_200_OK,
                        'data': serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return invalid_credentials()
        # return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)

# class DispatchDetailView(APIView):
#     serializer_class = DispatchSerializer

#     def put(self, request): TODO update state of dispatch


class DispatchListView(APIView):
    def get (self, request):
        if request.user.role == 'u':
            return invalid_credentials()
        date = str(timezone.localdate())
        print(date)
        dispatch = Dispatch.objects.filter(order__departure_date__gte=date).order_by('-pk')#https://gaussian37.github.io/python-django-django-query-set/
        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(dispatch, request)
        serializer = DispatchListSerializer(result_page, many=True, context={'request':request})
        return Response({
            'count': paginator.page.paginator.count,
            'results': serializer.data
            }
        )

