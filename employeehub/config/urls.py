"""
URL configuration for EmployeeHub project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employees.urls', namespace='employees')),
]

