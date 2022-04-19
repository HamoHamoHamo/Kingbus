from django.urls import path

from . import views

urlpatterns = [
    path('chat/room/<int:room_pk>',views.room, name='room'),
    path('chat/chatroomlist',views.chatroomList, name='chatroomlist'),
    path('chat',views.createChatroom),
]