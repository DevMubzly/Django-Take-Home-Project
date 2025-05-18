from django.urls import path
from . import views, teacher_views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('new/', views.course_create, name='course_create'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/new/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    
    # Teacher URLs
    path('teachers/register/', teacher_views.teacher_register, name='teacher_register'),
    path('teachers/profile/', teacher_views.teacher_profile, name='teacher_profile'),
    path('teachers/profile/edit/', teacher_views.teacher_profile_edit, name='teacher_profile_edit'),
    path('teachers/courses/', teacher_views.teacher_course_list, name='teacher_course_list'),
    path('teachers/courses/assign/', teacher_views.teacher_course_assign, name='teacher_course_assign'),
    path('teachers/courses/<int:course_id>/students/', teacher_views.teacher_course_students, name='teacher_course_students'),
    path('teachers/enrollments/<int:enrollment_id>/update-grade/', teacher_views.teacher_update_grade, name='teacher_update_grade'),
    path('dashboard/', teacher_views.user_dashboard, name='user_dashboard'),
]