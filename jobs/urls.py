from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/update/', views.job_update, name='job_update'),
    path('job/<int:job_id>/delete/', views.job_delete, name='job_delete'),
    path('job/<int:job_id>/submit_bid/', views.submit_bid, name='submit_bid'),
]
