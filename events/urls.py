from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('new/', views.event_create, name='event_create'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('register/<int:pk>/', views.event_register, name='event_register'),
    path('cancel/<int:pk>/', views.event_cancel_registration, name='event_cancel_registration'),
    path('my-events/', views.my_events, name='my_events'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
]