from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Enrollment
from django.core.exceptions import ValidationError
from django import forms
import re
from courses.models import Course

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

class StudentProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = Student
        fields = ('student_id', 'gender', 'date_of_birth', 'address', 'phone_number')
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not re.match(r'^[A-Z0-9]+$', student_id):
            raise ValidationError("Student ID must contain only uppercase letters and numbers")
        if Student.objects.filter(student_id=student_id).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.student_id != student_id):
                raise ValidationError("Student ID already exists")
        return student_id
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?[0-9]{10,15}$', phone_number):
            raise ValidationError("Enter a valid phone number")
        return phone_number

class EnrollmentForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    semester = forms.ChoiceField(
        choices=SEMESTER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Enrollment
        fields = ('course', 'semester', 'year')