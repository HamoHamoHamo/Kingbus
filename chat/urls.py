from django.urls import path

from . import views

urlpatterns = [
    path('room/<int:room_pk>',views.room, name='room'),
    path('chatroomlist',views.chatroomlist, name='chatroomlist'),
    path('',views.createchatroom),
]