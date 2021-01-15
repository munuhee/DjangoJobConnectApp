from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    ContactCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    public_profile,
    rate_post_view,
    PostSearchListView
)
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('',PostListView.as_view(), name="projects"),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    #path('checkout/', views.checkout, name="checkout"),
    #path('update_item/', views.updateItem, name="update_item"),
    #path('cart/', views.cart, name="cart"),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('new-post/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('profile/<str:username>', views.public_profile, name='public-profile'),
    path('post/<slug:slug>/<rating>', rate_post_view, name='rate_post'),
    path('category/<str:link>/', views.category, name="category"),
    #url(r'^search/$', views.search, name='search'),
    path('search/',PostSearchListView.as_view(), name="post_search_list_view"),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="core/sitemap.xml"),
    ),
]
