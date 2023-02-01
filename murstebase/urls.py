from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    path('sitemaps/', views.sitemaps, name='sitemaps'),
    path(
        ".well-known/pki-validation/8D9F2186D3C951419FEF6C64A2577C8B.txt",
        TemplateView.as_view(template_name="murstebase/8D9F2186D3C951419FEF6C64A2577C8B.txt"),
    ),
]
