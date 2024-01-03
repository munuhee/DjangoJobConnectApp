from django.urls import path
from . import views

app_name = "subscription"

urlpatterns = [
    path('subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    path('subscription/<int:pk>/', views.subscription_detail, name='subscription_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('cancel_payment/', views.cancel_payment, name='cancel_payment'),
]
