# Create your models here.
from django.db import models

class JobListing(models.Model):
    SOURCE_CHOICES = [
        ('LINKEDIN', 'LinkedIn'),
        ('INDEED', 'Indeed'),
        ('NAUKRI', 'Naukri'),
        ('INTERNSHALA', 'Internshala'),
    ]
    
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    url = models.URLField(max_length=1000)
    posted_date = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company} ({self.source})"
class userModel(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField()
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.username