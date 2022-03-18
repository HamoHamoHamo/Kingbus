from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# from rest_framework import viewsets

from .serializers import CompanyDetailSerializer, CompanyProfileViewSerializer, DriverDetailSerializer, DriverProfileViewSerializer, UserLoginSerializer, UserRegistrationSerializer, DriverRegistrationSerializer, CompanyRegistrationSerializer
from .models import User#, DriverAcc, CompanyAcc


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        username = request.GET.get('username')
        if username is not None:
            # if 'username' in request.GET:
            if len(username)>=4:
                try:
                    User.objects.get(username=username)
                    return Response({'result':'exists'},status=status.HTTP_409_CONFLICT)
                except ObjectDoesNotExist:
                    return Response({'result':'not exists'},status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

class CompanyLoginView(APIView):
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


class DriverAccDetailView(APIView):
    def get(self, request, **kwargs):
        if request.user.role == 'u':
            # driver = User.objects.get(id=kwargs['driver_id'])
            driver = get_object_or_404(User, id=kwargs['driver_id'])
            if hasattr(driver, 'driveracc'): #https://stackoverflow.com/questions/610883/how-to-know-if-an-object-has-an-attribute-in-python
                serializer = DriverProfileViewSerializer(driver)
                return Response(serializer.data)
            else:
                return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail':'Invalid Credentials.'}, status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['driver_id'])
        if user == request.user:
            if hasattr(user, 'driveracc'):
                driver = user.driveracc
                serializer = DriverDetailSerializer(driver, request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail':'Invalid Credentials.'}, status.HTTP_403_FORBIDDEN)


class CompanyAccDetailView(APIView):
    def get(self, request, **kwargs):
        if request.user.role == 'u':
            company = get_object_or_404(User, id=kwargs['company_id'])
            if hasattr(company, 'companyacc'):
                serializer = CompanyProfileViewSerializer(company)
                return Response(serializer.data)
            else:
                return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail':'Invalid Credentials.'}, status.HTTP_403_FORBIDDEN)

    
    def patch(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['company_id'])
        if user == request.user:
            if hasattr(user, 'companyacc'):
                company = user.companyacc
                serializer = CompanyDetailSerializer(company, request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail':'Invalid Credentials.'}, status.HTTP_403_FORBIDDEN)

