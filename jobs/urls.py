from django.conf.urls import url
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
    url(r'^job/(?P<pk>[\d]+)/delete/$', JobDelete.as_view(), name='job_delete'),
    url(r'^job/(?P<pk>[\d]+)/update/$', JobUpdate.as_view(), name='job_update'),
    url(r'^job/add/$', JobCreate.as_view(), name='job_add'),
    url(r'^job/(?P<pk>[\d]+)/$', JobDetail.as_view(), name='job_detail'),
    path('job-application/<int:pk>/update/', ApplicationUpdateView.as_view(), name='job-application-update'),
    path('job-application/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='job-application-delete'),
    path('job-application/<int:pk>/', ApplicationCreateView.as_view(), name='job-application-form'),
    path('search/',JobSearchListView.as_view(), name="job_search_list_view"),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="jobs/sitemap.xml"),
    ),
]
