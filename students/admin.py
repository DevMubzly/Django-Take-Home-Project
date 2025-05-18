from django.contrib import admin
from .models import Student, Enrollment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    fields = ('course', 'semester', 'year', 'grade', 'is_active')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_full_name', 'gender', 'phone_number', 'created_at')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('gender', 'created_at')
    inlines = [EnrollmentInline]
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'year', 'grade', 'is_active')
    list_filter = ('semester', 'year', 'grade', 'is_active')
    search_fields = ('student__student_id', 'student__user__first_name', 'student__user__last_name', 'course__code', 'course__title')
    list_editable = ('grade', 'is_active')
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course')
        }),
        ('Academic Details', {
            'fields': ('semester', 'year', 'grade', 'is_active')
        }),
    )
