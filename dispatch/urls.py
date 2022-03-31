from django.urls import path
from . import views

urlpatterns = [
    path('order',views.DispatchOrderView.as_view()),
    path('order/<int:order_id>',views.DispatchOrderDetailView.as_view()),
    path('order/list/u',views.DispatchOrderView.as_view()),

    path('order/list',views.DispatchListView.as_view()),
    # path('orders/<int:user_id>/old',views.),

    path('estimate',views.DispatchEstimateView.as_view()),
    path('estimate/<int:estimate_id>',views.DispatchEstimateDetailView.as_view()),
    path('estimate/list/u',views.DispatchEstimateView.as_view()),
    path('estimate/list/o/<int:order_id>',views.DispatchEstimateView.as_view()),

    path('dispatch',views.DispatchView.as_view()),

]