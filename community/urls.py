from django.urls import path
from . import views


urlpatterns = [
    path('board',views.PostView.as_view()),
    path('boardlist',views.PostListView.as_view()),
    path('board/<int:board_id>',views.PostDetailView.as_view()),

    path('board/comment',views.PostCommentView.as_view()),
    path('board/comment/<int:comment_id>',views.PostCommentView.as_view()),
    path('board/recomment',views.PostRecommentView.as_view()),
    path('board/recomment/<int:recomment_id>',views.PostRecommentView.as_view()),

    path('board/<int:board_id>/commentlist',views.PostCommentListView.as_view()),
]
