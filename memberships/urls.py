from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('simple-checkout/', views.simpleCheckout, name='simple_checkout'),
    path('homeplan/', views.plan, name='plan'),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('payment-complete/', views.paymentComplete, name='complete'),
    path('payment-done/', views.UserPlan, name='order'),
]