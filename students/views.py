from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm, StudentProfileForm, EnrollmentForm
from .models import Student, Enrollment
from courses.models import Course

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = StudentProfileForm()
    
    return render(request, 'students/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    # Check if user is a student
    if hasattr(request.user, 'student_profile'):
        student = get_object_or_404(Student, user=request.user)
        enrollments = Enrollment.objects.filter(student=student)
        
        return render(request, 'students/profile.html', {
            'student': student,
            'enrollments': enrollments
        })
    # If user is a teacher, redirect to teacher profile
    elif hasattr(request.user, 'teacher_profile'):
        return redirect('courses:teacher_profile')
    else:
        messages.error(request, 'Profile not found. Please complete registration.')
        return redirect('home')

@login_required
def profile_edit(request):
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:profile')
    else:
        form = StudentProfileForm(instance=student)
    
    return render(request, 'students/profile_edit.html', {'form': form})

@login_required
def enrollment_list(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    
    return render(request, 'students/enrollment_list.html', {'enrollments': enrollments})

@login_required
def enrollment_create(request):
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year']
            
            # Check if enrollment already exists
            if Enrollment.objects.filter(student=student, course=course, semester=semester, year=year).exists():
                messages.error(request, 'You are already enrolled in this course for the selected semester and year.')
            else:
                enrollment = form.save(commit=False)
                enrollment.student = student
                enrollment.save()
                messages.success(request, f'Successfully enrolled in {course.title}')
                return redirect('students:enrollment_list')
    else:
        form = EnrollmentForm()
    
    # Get courses that the student is not enrolled in
    enrolled_courses = Enrollment.objects.filter(student=student).values_list('course', flat=True)
    form.fields['course'].queryset = Course.objects.filter(is_active=True).exclude(id__in=enrolled_courses)
    
    return render(request, 'students/enrollment_create.html', {'form': form})

@login_required
def enrollment_detail(request, pk):
    student = get_object_or_404(Student, user=request.user)
    enrollment = get_object_or_404(Enrollment, pk=pk, student=student)
    
    return render(request, 'students/enrollment_detail.html', {'enrollment': enrollment})
