from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Experience, Education, Contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'profiles/register.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.profile
            print("profile exists")
        except Profile.DoesNotExist:
            profile = None
        experiences = Experience.objects.filter(profile=profile)
        education = Education.objects.filter(profile=profile).first()
        contact = Contact.objects.filter(profile=profile).first()
        context.update({
            'profile': profile,
            'experiences': experiences,
            'education': education,
            'contact': contact
        })
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile
