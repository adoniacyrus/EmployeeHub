from decimal import Decimal
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


class Employee(models.Model):
    """
    Employee Model representing staff details in EmployeeHub.
    Includes comprehensive personal, organizational and compensation fields.
    """

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
    ]

    phone_regex = RegexValidator(
        regex=r'^[0-9+\-\s()]{7,20}$',
        message="Phone number must contain between 7 and 20 valid characters (digits, +, -, parentheses)."
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="Full Name",
        help_text="Enter employee's full legal name."
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Email Address",
        help_text="Unique corporate or personal email address."
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        verbose_name="Contact Number",
        help_text="Valid contact number."
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male',
        verbose_name="Gender"
    )
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='IT',
        verbose_name="Department"
    )
    designation = models.CharField(
        max_length=100,
        verbose_name="Designation",
        help_text="Job title or role (e.g. Software Engineer, HR Specialist)."
    )
    joining_date = models.DateField(
        verbose_name="Joining Date",
        help_text="Date the employee joined the organization."
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), message="Salary must be greater than zero.")],
        verbose_name="Monthly Salary",
        help_text="Monthly compensation amount."
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Address",
        help_text="Residential or correspondence address."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        db_table = 'employees_employee'
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.full_name} ({self.designation} - {self.department})"

