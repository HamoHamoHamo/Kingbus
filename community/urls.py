from django.urls import path
from . import views


urlpatterns = [
    path('',views.PostView.as_view()),
    path('<int:board_id>',views.PostDetailView.as_view()),
]
