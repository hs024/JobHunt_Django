from django.contrib import admin
from scraper.models import JobListing  ,userModel
# Register your models here.

class JobListingModelAdmin(admin.ModelAdmin):
    list_display=["id","title","posted_date","location","url","description","salary","skills","is_active"]
admin.site.register(JobListing,JobListingModelAdmin)
class userModelAdmin(admin.ModelAdmin):
    list_display=["id","username","email","password"]
admin.site.register(userModel,userModelAdmin)
