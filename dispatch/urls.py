from django.urls import path
from . import views

urlpatterns = [
    path('orders/',views.DispatchOrderView.as_view()),
    path('orders/<int:order_id>',views.DispatchOrderDetailView.as_view()),
    # path('orders/',views.PostOrders.as_view(),name='order'),
    # path('orders/<int:user_id>/old',views.),
    # path('orders/<int:user_id>/ing',views.),
]