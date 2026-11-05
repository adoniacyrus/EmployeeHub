from decimal import Decimal
from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    """
    Form for registering and updating employees.
    Configured with Bootstrap 5 classes, clear placeholders, and robust validation.
    """

    class Meta:
        model = Employee
        fields = [
            'full_name',
            'email',
            'phone',
            'gender',
            'department',
            'designation',
            'joining_date',
            'salary',
            'address',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. John Doe',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. john.doe@example.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +1 555-0199 or 9876543210',
                'required': True,
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Senior Software Engineer',
                'required': True,
            }),
            'joining_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True,
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 75000.00',
                'step': '0.01',
                'min': '0.01',
                'required': True,
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter street address, city, and postal code...',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        # Verify email uniqueness for new records or when changing an existing record
        query = Employee.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("An employee with this email address is already registered.")
        return email

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= Decimal('0'):
            raise forms.ValidationError("Salary must be a positive value greater than zero.")
        return salary

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if len(full_name) < 2:
            raise forms.ValidationError("Full name must be at least 2 characters long.")
        return full_name

