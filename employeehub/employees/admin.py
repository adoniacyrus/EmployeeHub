from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'phone',
        'department',
        'designation',
        'joining_date',
        'salary',
        'created_at',
    )
    list_filter = ('department', 'gender', 'joining_date')
    search_fields = ('full_name', 'email', 'designation', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

