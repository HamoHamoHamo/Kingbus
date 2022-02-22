from django.urls import path
from . import views

urlpatterns = [
    path('orders/',views.DispatchOrderView.as_view()),
    path('orders/<int:order_id>/',views.DispatchOrderDetailView.as_view()),
    path('orders/u/<int:user_id>/',views.DispatchOrderView.as_view()),
    # path('orders/<int:user_id>/old',views.),

    path('estimate/',views.DispatchEstimateView.as_view()),
    path('estimate/<int:estimate_id>/',views.DispatchEstimateDetailView.as_view()),
    path('estimate/<int:order_id>/list/',views.DispatchEstimateView.as_view()),
]