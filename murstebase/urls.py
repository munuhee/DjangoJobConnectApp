from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sitemaps/', views.sitemaps, name='sitemaps'),
]
