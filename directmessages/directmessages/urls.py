from django.urls import path
from . import views
from .views import MessageCreateView, InboxListView

# second- truncated request is sent here and a match is searched for in url patterns again
urlpatterns = [
    path('new/<username>', MessageCreateView.as_view(), name='message-form'),
    path('inbox/', InboxListView.as_view(), name='inbox-list'),
]
