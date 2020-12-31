from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .forms import MessageForm
from .models import Message, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from notifications.signals import notify


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):  # modifys the default sucess url to return the page the submission came from
        return self.request.path

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = User.objects.get(username=self.kwargs['username'])  # ['username'] is the username assigned by to the message button in the public profile.html. we are making the instance of the form assign the receiver field of the message model to the username object whos username=self.kwargs['username'] which is the storage location of url parameters
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receiver_message_objects'] = Message.objects.filter(Q(receiver=self.request.user) & Q(sender__username=self.kwargs['username']) | Q(receiver__username=self.kwargs['username']) & Q(sender=self.request.user))
        # context['receiver_username'] =
        return context


class InboxListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender_list_author = []
        sender_qs = []
        qs = Message.objects.filter(receiver=self.request.user).order_by('-date_created')  # all messages send to logged in user
        for i in qs:
            if i.sender.username not in sender_list_author:
                sender_list_author.append(i.sender.username)  # sender_list is a list of unique authors in the qs
                sender_qs.append(i)
        context['sender_qs'] = sender_qs
        return context

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by('-date_created')
