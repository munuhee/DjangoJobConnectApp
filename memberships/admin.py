from django.contrib import admin
from . models import *
# Register your models here.

@admin.register(Plan)
class Plan(admin.ModelAdmin):
    list_display = ('plan_type', 'price')


@admin.register(UserPlan)
class UserPlan(admin.ModelAdmin):
    list_display = ('user','plan', 'date_subscribed')
