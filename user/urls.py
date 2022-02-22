from django.urls import path#, include
# from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from . import views

# routers = routers.DefaultRouter()
# routers.register('user', views.UserView, 'user')
# routers.register('driver', views.DriverAccView, 'driver')

urlpatterns = [
    # path('api/', include(routers.urls)),
    path('users/register/', views.createUser),
    path('drivers/register/', views.DriverAccRegisterView.as_view()),
    path('companys/register/', views.CompanyAccRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    # path('drivers/login/', views.DriverLoginView.as_view()),
    # path('companys/login/', views.CompanyLoginView.as_view()),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]