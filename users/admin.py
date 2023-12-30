from django.contrib import admin
from .models import Profile, Experience, Education, Contact

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_status')
    search_fields = ('user__username', 'job_status')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'company', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'title', 'company')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'degree', 'institution', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'degree', 'institution')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('profile', 'email', 'linkedin', 'twitter')
    search_fields = ('profile__user__username', 'email', 'linkedin', 'twitter')
