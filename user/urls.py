from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from . import views

routers = routers.DefaultRouter()
routers.register('user', views.UserView, 'user')
routers.register('driver', views.DriverAccView, 'driver')

urlpatterns = [
    path('api/', include(routers.urls)),
    path('create/', views.createUser),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]