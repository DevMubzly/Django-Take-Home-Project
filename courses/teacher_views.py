from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from .forms import TeacherRegistrationForm, TeacherProfileForm, CourseAssignmentForm
from .models import Teacher, Course
from students.models import Student, Enrollment

def teacher_register(request):
    if request.method == 'POST':
        user_form = TeacherRegistrationForm(request.POST)
        profile_form = TeacherProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            messages.success(request, 'Teacher registration successful!')
            return redirect('home')
    else:
        user_form = TeacherRegistrationForm()
        profile_form = TeacherProfileForm()
    
    return render(request, 'courses/teacher_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    
    return render(request, 'courses/teacher_profile.html', {
        'teacher': teacher,
        'courses': courses
    })

@login_required
def teacher_profile_edit(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('courses:teacher_profile')
    else:
        form = TeacherProfileForm(instance=teacher)
    
    return render(request, 'courses/teacher_profile_edit.html', {'form': form})

@login_required
def teacher_course_list(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    
    return render(request, 'courses/teacher_course_list.html', {'courses': courses})

@login_required
def teacher_course_assign(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    
    if request.method == 'POST':
        form = CourseAssignmentForm(request.POST, teacher=teacher)
        if form.is_valid():
            course = form.cleaned_data['course']
            course.teacher = teacher
            course.save()
            messages.success(request, f'Successfully assigned to {course.title}')
            return redirect('courses:teacher_course_list')
    else:
        form = CourseAssignmentForm(teacher=teacher)
    
    return render(request, 'courses/teacher_course_assign.html', {'form': form})

@login_required
def teacher_course_students(request, course_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher)
    enrollments = Enrollment.objects.filter(course=course)
    
    return render(request, 'courses/teacher_course_students.html', {
        'course': course,
        'enrollments': enrollments
    })

@login_required
def teacher_update_grade(request, enrollment_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, course__teacher=teacher)
    
    if request.method == 'POST':
        grade = request.POST.get('grade')
        course_id = request.POST.get('course_id') or enrollment.course.id
        if grade in dict(Enrollment.GRADE_CHOICES):
            enrollment.grade = grade
            enrollment.save()
            messages.success(request, f'Grade updated for {enrollment.student}')
        else:
            messages.error(request, 'Invalid grade')
        return redirect('courses:teacher_course_students', course_id=course_id)
    
    return render(request, 'courses/teacher_update_grade.html', {'enrollment': enrollment})

@login_required
def is_teacher(user):
    return hasattr(user, 'teacher_profile')

@login_required
def is_student(user):
    return hasattr(user, 'student_profile')

def user_dashboard(request):
    if is_teacher(request.user):
        return redirect('courses:teacher_profile')
    elif is_student(request.user):
        return redirect('students:profile')
    else:
        messages.info(request, 'Please complete your profile setup')
        return redirect('home')