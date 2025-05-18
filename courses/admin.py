from django.contrib import admin
from .models import Department, Course

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1
    fields = ('code', 'title', 'level', 'credits', 'is_active')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)
    inlines = [CourseInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'level', 'credits', 'is_active')
    list_filter = ('department', 'level', 'is_active')
    search_fields = ('code', 'title', 'description')
    list_editable = ('is_active',)
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'code', 'department', 'level')
        }),
        ('Details', {
            'fields': ('credits', 'description', 'is_active')
        }),
    )
