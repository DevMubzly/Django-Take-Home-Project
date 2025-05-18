from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(regex='^[A-Z0-9]+$', message='Student ID must contain only uppercase letters and numbers')
    ])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    enrolled_courses = models.ManyToManyField(Course, through='Enrollment', related_name='enrolled_students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True)
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'course', 'semester', 'year']
        
    def __str__(self):
        return f"{self.student} - {self.course} ({self.semester} {self.year})"
