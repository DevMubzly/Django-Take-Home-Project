# Student Portal Django Project

This project is a comprehensive student portal web application built with Django. It provides functionality for managing courses, student information, and campus events.

## Project Structure

The project consists of three main applications:

1. **Courses App**
   - Manages departments and courses
   - Models: Department, Course
   - Relationships: Department has many Courses

2. **Students App**
   - Manages student profiles and course enrollments
   - Models: Student, Enrollment
   - Relationships: Student has many Courses through Enrollment

3. **Events App**
   - Manages campus events and registrations
   - Models: EventCategory, Event, EventRegistration
   - Relationships: Events belong to Categories, Users register for Events

## Features

- User registration and authentication
- Course management and enrollment
- Student profile management
- Event creation and registration
- Custom admin interfaces
- Form validation and error handling
- Responsive design with CSS styling

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`

## Models

### Courses App
- **Department**: Represents academic departments
- **Course**: Represents courses offered by departments

### Students App
- **Student**: Extends the User model with additional student information
- **Enrollment**: Represents a student's enrollment in a course

### Events App
- **EventCategory**: Categories for different types of events
- **Event**: Campus events with details like location, time, etc.
- **EventRegistration**: Tracks user registration and attendance for events

## Admin Customization

Each model has custom admin classes with:
- List displays for important fields
- Search functionality
- Filtering options
- Inline editing for related models

## Forms

The application includes forms for:
- User registration and login
- Student profile creation and editing
- Course enrollment
- Event registration

## Data Validation

The application implements validation for:
- Student ID format
- Date ranges for events
- Enrollment constraints
- Form input validation with error messages

## Template Customization

The project uses custom templates with:
- Base template with inheritance
- Responsive design
- CSS styling
- Form rendering
- Error message display

## Project Requirements Fulfilled

- At least 3 apps/pages (Courses, Students, Events)
- At least 2 models per app with defined relationships
- Custom model admin classes
- Forms for creating/updating models
- User registration and authentication
- Custom templating and styling
- Data validation and error handling
- Comprehensive documentation