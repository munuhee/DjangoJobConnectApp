from django.contrib import admin
from .models import *
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'pub_date', 'author',  'budget')
admin.site.register(Job, JobAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'content','author', 'budget', 'date_created')
admin.site.register(Application, ApplicationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Requirement, RequirementAdmin)
