from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/new/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/', views.enrollment_detail, name='enrollment_detail'),
]