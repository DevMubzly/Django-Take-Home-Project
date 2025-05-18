from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, Course
from .forms import DepartmentForm, CourseForm

def course_list(request):
    courses = Course.objects.all().order_by('department', 'title')
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def course_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create courses.')
        return redirect('courses:course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create Course'})

@login_required
def course_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit courses.')
        return redirect('courses:course_list')
    
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})

def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'courses/department_list.html', {'departments': departments})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    courses = Course.objects.filter(department=department).order_by('title')
    return render(request, 'courses/department_detail.html', {
        'department': department,
        'courses': courses
    })

@login_required
def department_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create departments.')
        return redirect('courses:department_list')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('courses:department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'courses/department_form.html', {'form': form, 'title': 'Create Department'})

@login_required
def department_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit departments.')
        return redirect('courses:department_list')
    
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('courses:department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'courses/department_form.html', {'form': form, 'title': 'Edit Department'})
