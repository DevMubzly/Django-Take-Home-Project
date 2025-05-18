from django import forms
from .models import EventCategory, Event, EventRegistration
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ('name', 'description')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'category', 'department', 'location', 
                 'start_date', 'end_date', 'registration_deadline', 'max_participants', 'status')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        registration_deadline = cleaned_data.get('registration_deadline')
        
        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be after start date")
        
        if registration_deadline and start_date and registration_deadline > start_date:
            raise ValidationError("Registration deadline must be before the event starts")
        
        if registration_deadline and registration_deadline < timezone.now():
            raise ValidationError("Registration deadline cannot be in the past")
        
        return cleaned_data

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ('event',)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        # Only show events that are upcoming and haven't reached registration deadline
        self.fields['event'].queryset = Event.objects.filter(
            status='upcoming',
            registration_deadline__gt=timezone.now()
        )
    
    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        
        if event:
            # Check if user is already registered
            if EventRegistration.objects.filter(event=event, user=self.user).exists():
                raise ValidationError("You are already registered for this event")
            
            # Check if event is full
            if event.eventregistration_set.count() >= event.max_participants:
                raise ValidationError("This event has reached maximum capacity")
        
        return cleaned_data