from django.db import models
from django.contrib.auth.models import User
from courses.models import Department
from django.core.validators import MinValueValidator

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Event Categories'
    
    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_events', null=True, blank=True)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    max_participants = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    participants = models.ManyToManyField(User, through='EventRegistration', related_name='registered_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    ATTENDANCE_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('absent', 'Absent'),
        ('cancelled', 'Cancelled'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    attendance_status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='registered')
    feedback = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['event', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
