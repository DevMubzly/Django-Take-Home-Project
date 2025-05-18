from django import forms
from .models import Department, Course, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'code', 'description')
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Department.objects.filter(code=code).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.code != code):
                raise ValidationError("Department code already exists")
        return code

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'code', 'department', 'level', 'credits', 'description', 'is_active', 'teacher')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Course.objects.filter(code=code).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.code != code):
                raise ValidationError("Course code already exists")
        return code
    
    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits < 1 or credits > 6:
            raise ValidationError("Credits must be between 1 and 6")
        return credits

class TeacherRegistrationForm(UserCreationForm):
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

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('teacher_id', 'department', 'qualification', 'bio')
    
    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get('teacher_id')
        if not re.match(r'^[A-Z0-9]+$', teacher_id):
            raise ValidationError("Teacher ID must contain only uppercase letters and numbers")
        if Teacher.objects.filter(teacher_id=teacher_id).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.teacher_id != teacher_id):
                raise ValidationError("Teacher ID already exists")
        return teacher_id

class CourseAssignmentForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super(CourseAssignmentForm, self).__init__(*args, **kwargs)
        
        if teacher:
            # Filter courses by teacher's department
            self.fields['course'].queryset = Course.objects.filter(
                is_active=True,
                department=teacher.department,
                teacher__isnull=True  # Only show unassigned courses
            )