from django.urls import path
from scraper import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('login/',views.userlogin,name="login"),
    path('register/', views.register, name='register'),
]