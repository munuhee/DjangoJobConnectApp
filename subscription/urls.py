from django.urls import path
from . import views

urlpatterns = [
    path('subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    path('subscription/<int:pk>/', views.subscription_detail, name='subscription_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    # Add a URL for the cancel_payment view if needed
    # path('cancel_payment/', views.cancel_payment, name='cancel_payment'),
    # Other URL patterns for your app
    # ...
]
