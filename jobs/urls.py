from django.urls import re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import (
    JobDetail,
    JobCreate,
    JobUpdate,
    JobDelete,
    Home,
    ApplicationCreateView,
    ApplicationUpdateView,
    ApplicationDeleteView,
    JobSearchListView
    #JobCategory,
    #Dashboard
)
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    #url(r'^job/cat/(?P<pk>[\d]+)/$', JobCategory.as_view(), name='job_by_category'),
    path('jobscategory/<str:link>/', views.jobscategory, name="jobscategory"),
    path('',Home.as_view(), name="jobs"),
    path('job/<int:pk>/delete/', views.JobDelete.as_view(), name='job_delete'),
    path('job/<int:pk>/update/', views.JobUpdate.as_view(), name='job_update'),
    path('job/add/', views.JobCreate.as_view(), name='job_add'),
    path('job/<int:pk>/', views.JobDetail.as_view(), name='job_detail'),
    path('job-application/<int:pk>/update/', ApplicationUpdateView.as_view(), name='job-application-update'),
    path('job-application/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='job-application-delete'),
    path('job-application/<int:pk>/', ApplicationCreateView.as_view(), name='job-application-form'),
    path('search/',JobSearchListView.as_view(), name="job_search_list_view"),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="jobs/sitemap.xml"),
    ),
]
