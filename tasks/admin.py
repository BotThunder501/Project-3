from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'status', 'created_at', 'updated_at')
    list_filter = ('priority', 'status', 'due_date')
    search_fields = ('title', 'description')
    list_editable = ('priority', 'status')  # Allow editing priority and status directly from the list view
    date_hierarchy = 'due_date'  # Add a date-based navigation hierarchy by due date