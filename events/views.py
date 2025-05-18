from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import EventCategory, Event, EventRegistration
from .forms import EventCategoryForm, EventForm, EventRegistrationForm

def event_list(request):
    events = Event.objects.all().order_by('start_date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_registered = False
    if request.user.is_authenticated:
        user_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_registered': user_registered
    })

@login_required
def event_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create events.')
        return redirect('events:event_list')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit events.')
        return redirect('events:event_list')
    
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event'})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Check if registration is still open
    if event.registration_deadline < timezone.now():
        messages.error(request, 'Registration for this event has closed.')
        return redirect('events:event_detail', pk=event.pk)
    
    # Check if event is full
    if EventRegistration.objects.filter(event=event).count() >= event.max_participants:
        messages.error(request, 'This event has reached maximum capacity.')
        return redirect('events:event_detail', pk=event.pk)
    
    # Check if user is already registered
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.info(request, 'You are already registered for this event.')
        return redirect('events:event_detail', pk=event.pk)
    
    # Register the user
    EventRegistration.objects.create(event=event, user=request.user)
    messages.success(request, 'You have successfully registered for this event!')
    return redirect('events:event_detail', pk=event.pk)

@login_required
def event_cancel_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = get_object_or_404(EventRegistration, event=event, user=request.user)
    
    registration.attendance_status = 'cancelled'
    registration.save()
    
    messages.success(request, 'Your registration has been cancelled.')
    return redirect('events:event_detail', pk=event.pk)

@login_required
def my_events(request):
    registrations = EventRegistration.objects.filter(user=request.user).order_by('event__start_date')
    return render(request, 'events/my_events.html', {'registrations': registrations})

def category_list(request):
    categories = EventCategory.objects.all().order_by('name')
    return render(request, 'events/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(EventCategory, pk=pk)
    events = Event.objects.filter(category=category).order_by('start_date')
    return render(request, 'events/category_detail.html', {
        'category': category,
        'events': events
    })

@login_required
def category_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create categories.')
        return redirect('events:category_list')
    
    if request.method == 'POST':
        form = EventCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('events:category_list')
    else:
        form = EventCategoryForm()
    
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Create Category'})

@login_required
def category_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit categories.')
        return redirect('events:category_list')
    
    category = get_object_or_404(EventCategory, pk=pk)
    
    if request.method == 'POST':
        form = EventCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('events:category_detail', pk=category.pk)
    else:
        form = EventCategoryForm(instance=category)
    
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Edit Category'})
