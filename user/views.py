from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import UserSerializer, DriverSerializer
from .models import User, DriverAcc#, CompanyAcc


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class DriverAccView(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = DriverAcc.objects.all()
    permission_classes = [AllowAny]


# class UserView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)