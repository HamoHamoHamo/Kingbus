from django.urls import path, include
from rest_framework import routers
from main import views

routers = routers.DefaultRouter()
routers.register('Test', views.TestView, 'Test')

urlpatterns = [
    path('api/', include(routers.urls))
]