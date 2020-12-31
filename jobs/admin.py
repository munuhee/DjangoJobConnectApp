from django.contrib import admin
from .models import Job, Application


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author',  'budget','jobscategory')



class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'content','author', 'budget', 'date_created')


admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
