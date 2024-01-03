from django.contrib import admin
from .models import Category, Requirement, Job, Bid

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'pub_date')
    list_filter = ('pub_date', 'categories', 'requirements')
    search_fields = ('job_title', 'company_name')
    date_hierarchy = 'pub_date'
    filter_horizontal = ('categories', 'requirements')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('job', 'bidder', 'bid_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job__job_title', 'bidder__username')

    def job(self, obj):
        return obj.job.job_title

    def bidder(self, obj):
        return obj.bidder.username
