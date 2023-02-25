from django.contrib import admin
from .models import Profile, Experience, Education, Contact

class ExperienceInline(admin.TabularInline):
    model = Experience

class EducationInline(admin.TabularInline):
    model = Education

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('profile', 'email', 'linkedin', 'twitter')

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = [
        ExperienceInline,
        EducationInline,
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact, ContactAdmin)
