from decimal import Decimal
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import Employee
from .forms import EmployeeForm


class EmployeeCRUDTests(TestCase):
    """
    Automated test suite verifying the fundamental CRUD operations,
    form validations, search, filtering, and dashboard statistics for EmployeeHub.
    """

    def setUp(self):
        self.client = Client()
        self.sample_employee = Employee.objects.create(
            full_name="Alice Johnson",
            email="alice.johnson@example.com",
            phone="+1-555-0101",
            gender="Female",
            department="IT",
            designation="Software Engineer",
            joining_date=date(2023, 1, 15),
            salary=Decimal("85000.00"),
            address="123 Tech Lane, Silicon City"
        )

    def test_01_create_employee(self):
        """Test 1: CREATE operation - Verify employee is saved in database."""
        post_data = {
            'full_name': 'Bob Smith',
            'email': 'bob.smith@example.com',
            'phone': '+1-555-0102',
            'gender': 'Male',
            'department': 'Finance',
            'designation': 'Financial Analyst',
            'joining_date': '2023-03-01',
            'salary': '72000.00',
            'address': '456 Wall Street',
        }
        response = self.client.post(reverse('employees:employee_create'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirects to list view
        self.assertTrue(Employee.objects.filter(email='bob.smith@example.com').exists())
        bob = Employee.objects.get(email='bob.smith@example.com')
        self.assertEqual(bob.full_name, 'Bob Smith')
        self.assertEqual(bob.department, 'Finance')
        self.assertEqual(bob.salary, Decimal('72000.00'))

    def test_02_read_employee_list_and_detail(self):
        """Test 2: READ operation - Verify list and detail views render employee data."""
        # List view
        list_response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Alice Johnson")
        self.assertContains(list_response, "Software Engineer")

        # Detail view
        detail_response = self.client.get(
            reverse('employees:employee_detail', args=[self.sample_employee.pk])
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Alice Johnson")
        self.assertContains(detail_response, "alice.johnson@example.com")
        self.assertContains(detail_response, "123 Tech Lane")

    def test_03_update_employee(self):
        """Test 3: UPDATE operation - Modify department, designation, salary and verify changes."""
        update_data = {
            'full_name': 'Alice Johnson',
            'email': 'alice.johnson@example.com',
            'phone': '+1-555-0101',
            'gender': 'Female',
            'department': 'Operations',       # Changed from IT
            'designation': 'Operations Lead',  # Changed from Software Engineer
            'joining_date': '2023-01-15',
            'salary': '95000.00',              # Changed from 85000.00
            'address': '123 Tech Lane, Silicon City'
        }
        response = self.client.post(
            reverse('employees:employee_update', args=[self.sample_employee.pk]),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        self.sample_employee.refresh_from_db()
        self.assertEqual(self.sample_employee.department, 'Operations')
        self.assertEqual(self.sample_employee.designation, 'Operations Lead')
        self.assertEqual(self.sample_employee.salary, Decimal('95000.00'))

    def test_04_delete_employee(self):
        """Test 4: DELETE operation - Delete employee and verify database removal."""
        pk = self.sample_employee.pk
        # GET renders confirmation page
        get_response = self.client.get(reverse('employees:employee_delete', args=[pk]))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, "Alice Johnson")

        # POST performs actual deletion
        post_response = self.client.post(reverse('employees:employee_delete', args=[pk]))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Employee.objects.filter(pk=pk).exists())

    def test_duplicate_email_validation(self):
        """Verify that duplicate email addresses are rejected."""
        form_data = {
            'full_name': 'Duplicate User',
            'email': 'alice.johnson@example.com',  # Existing email
            'phone': '+1-555-0199',
            'gender': 'Male',
            'department': 'HR',
            'designation': 'HR Executive',
            'joining_date': '2024-01-01',
            'salary': '50000.00',
            'address': 'Some Address'
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_positive_salary_validation(self):
        """Verify that negative or zero salary values are rejected."""
        form_data = {
            'full_name': 'Negative Salary User',
            'email': 'negative@example.com',
            'phone': '+1-555-0199',
            'gender': 'Male',
            'department': 'HR',
            'designation': 'Recruiter',
            'joining_date': '2024-01-01',
            'salary': '-1000.00',
            'address': 'Some Address'
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('salary', form.errors)

    def test_search_functionality(self):
        """Verify searching employees by full name and email."""
        Employee.objects.create(
            full_name="Carol Danvers",
            email="carol.danvers@example.com",
            phone="+1-555-0103",
            gender="Female",
            department="HR",
            designation="HR Manager",
            joining_date=date(2022, 6, 1),
            salary=Decimal("90000.00")
        )

        # Search by name "Carol"
        res1 = self.client.get(reverse('employees:employee_list') + '?q=Carol')
        self.assertContains(res1, "Carol Danvers")
        self.assertNotContains(res1, "Alice Johnson")

        # Search by email "alice"
        res2 = self.client.get(reverse('employees:employee_list') + '?q=alice')
        self.assertContains(res2, "Alice Johnson")
        self.assertNotContains(res2, "Carol Danvers")

    def test_department_filtering(self):
        """Verify filtering employees by department."""
        Employee.objects.create(
            full_name="David Marketing",
            email="david.marketing@example.com",
            phone="+1-555-0104",
            gender="Male",
            department="Marketing",
            designation="Brand Specialist",
            joining_date=date(2023, 5, 10),
            salary=Decimal("65000.00")
        )

        res = self.client.get(reverse('employees:employee_list') + '?department=Marketing')
        self.assertContains(res, "David Marketing")
        self.assertNotContains(res, "Alice Johnson")

    def test_dashboard_statistics(self):
        """Verify dynamic database aggregation on the Dashboard."""
        Employee.objects.create(
            full_name="Eve Finance",
            email="eve.finance@example.com",
            phone="+1-555-0105",
            gender="Female",
            department="Finance",
            designation="Accountant",
            joining_date=date(2023, 8, 12),
            salary=Decimal("68000.00")
        )

        response = self.client.get(reverse('employees:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Total employees should be 2 (Alice + Eve)
        self.assertEqual(response.context['total_employees'], 2)
        # 2 distinct departments (IT and Finance)
        self.assertEqual(response.context['total_departments'], 2)
        # Both appear in recent list
        self.assertEqual(len(response.context['recent_employees']), 2)

