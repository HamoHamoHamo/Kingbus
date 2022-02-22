from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from dispatch.models import Dispatch
from .serializers import DispatchOrderSerializer#, DispatchOrderDetailSerializer

class DispatchOrderView(APIView):
    serializer_class = DispatchOrderSerializer
    # permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        else:
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Dispatch successfully created!',
                'dispatch': serializer.validated_data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class DispatchOrderDetailView(APIView):
    serializer_class = DispatchOrderSerializer

    def get(self, request):
        return self.serializer_class(Dispatch.objects.all)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
