from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post/create/', views.post_create, name='post-create'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('post/<slug:slug>/update/', views.post_update, name='post-update'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post-delete'),
    path('user/<str:username>/', views.user_post_list, name='user-post-list'),
    path('category/<str:link>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('profile/<str:username>/', views.public_profile, name='public-profile'),
    path('rate/<slug:slug>/<int:rating>/', views.rate_post_view, name='rate-post'),
    path('comment/<slug:slug>/', views.comment, name='comment'),
    path('contact/', views.contact_create, name='contact-create'),
    path('search-list/', views.post_search_list, name='search-list'),
]
