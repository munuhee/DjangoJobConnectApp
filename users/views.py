from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Experience, Education, Contact
from .forms import ExperienceForm, EducationForm, ContactForm, ProfileForm

def register_view(request):
    """
    View for user registration.
    Uses Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def profile_view(request, username):
    """
    Display user profile, experiences, education, and contact details.

    Renders the user's profile page showing their details, experiences, education,
    and contact information based on the provided username. If the user doesn’t exist,
    returns a 404 error.
    """
    user_profile = get_object_or_404(Profile, user__username=username)
    experiences = Experience.objects.filter(profile=user_profile).order_by('-start_date')
    educations = Education.objects.filter(profile=user_profile).order_by('-start_date')
    contact_info = Contact.objects.select_related('profile').filter(profile=user_profile).first()
    
    context = {
            'user_profile': user_profile,
            'experiences': experiences,
            'educations': educations,
            'contact_info': contact_info,
    }
    
    is_own_profile = False
    if request.user.is_authenticated and request.user == user_profile.user:
        is_own_profile = True
        return render(request, 'users/profile.html', context)
    return render(request, 'users/public_profile.html', context)

@login_required
def profile_edit_view(request, username):
    """
    Edit user profile, experiences, education, and contact details.

    GET:
    Renders forms to edit user details.

    POST:
    Updates profile, experiences, education, and contact details if valid;
    Redirects to the user's profile page on success, re-renders the edit
    page with errors if forms are invalid.
    """
    user_profile = get_object_or_404(Profile, user__username=username)
    
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, instance=user_profile)
        experience_form = ExperienceForm(data=request.POST)
        education_form = EducationForm(data=request.POST)
        contact_form = ContactForm(data=request.POST)

        if profile_form.is_valid() and experience_form.is_valid() and education_form.is_valid() and contact_form.is_valid():
            profile_form.save()
            experience = experience_form.save(commit=False)
            experience.profile = user_profile
            experience.save()
            education = education_form.save(commit=False)
            education.profile = user_profile
            education.save()
            contact = contact_form.save(commit=False)
            contact.profile = user_profile
            contact.save()
            return redirect('profile', username=username)
    else:
        profile_form = ProfileForm(instance=user_profile)
        experience_form = ExperienceForm()
        education_form = EducationForm()
        contact_form = ContactForm()

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'experience_form': experience_form,
        'education_form': education_form,
        'contact_form': contact_form,
    }

    return render(request, 'users/profile_edit.html', context)
