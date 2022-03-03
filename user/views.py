from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# from rest_framework import viewsets
from .serializers import UserLoginSerializer, UserRegistrationSerializer, DriverRegistrationSerializer, CompanyRegistrationSerializer
# from .models import User, DriverAcc, CompanyAcc


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    # post아님?
    # https://velog.io/@jch9537/REST-API-LogIn-GET-vs-POST
    # POST가 맞는듯
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'username': serializer.validated_data['username'],
                    #name 추가
                    'name': serializer.validated_data['name'],
                    'role': serializer.validated_data['role']
                }
            }
            return Response(response, status=status_code)

'''
class DriverLoginView(APIView):
    serializer_class = DriverLoginSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                    # 'role': serializer.data['role']
                }
            }
            return Response(response, status=status_code)


class CompanyLoginView(APIView):
    serializer_class = CompanyLoginSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                    # 'role': serializer.data['role']
                }
            }
            return Response(response, status=status_code)
'''

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        # if not User.objects.filter(email=serializer.validated_data['email']).first() is None:
            # return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)
        else:
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class DriverAccRegisterView(APIView):
    serializer_class = DriverRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        else:
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'User successfully registered!',
                'user': serializer.validated_data['username'],
            }
            return Response(response, status=status.HTTP_201_CREATED)


class CompanyAccRegisterView(APIView):
    serializer_class = CompanyRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        else:
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'User successfully registered!',
                'user': serializer.validated_data['username'],
            }
            return Response(response, status=status.HTTP_201_CREATED)

