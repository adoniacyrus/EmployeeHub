from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Employee
from .forms import EmployeeForm


def dashboard(request):
    """
    Dashboard View:
    Computes real-time dynamic organizational analytics:
    - Total Headcount
    - Active Department Count & Breakdown
    - 5 Most Recently Onboarded Employees
    - Total Monthly Payroll Budget & Average Compensation
    """
    total_employees = Employee.objects.count()
    distinct_departments_count = Employee.objects.values('department').distinct().count()
    recent_employees = Employee.objects.all().order_by('-created_at')[:5]
    
    dept_distribution = (
        Employee.objects.values('department')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Calculate workforce metrics
    payroll_stats = Employee.objects.aggregate(
        total_payroll=Sum('salary'),
        avg_salary=Avg('salary')
    )
    total_payroll = payroll_stats['total_payroll'] or Decimal('0.00')
    avg_salary = payroll_stats['avg_salary'] or Decimal('0.00')

    gender_distribution = (
        Employee.objects.values('gender')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_employees': total_employees,
        'total_departments': distinct_departments_count,
        'all_department_choices': Employee.DEPARTMENT_CHOICES,
        'recent_employees': recent_employees,
        'dept_distribution': dept_distribution,
        'total_payroll': total_payroll,
        'avg_salary': avg_salary,
        'gender_distribution': gender_distribution,
    }
    return render(request, 'employees/dashboard.html', context)


def employee_list(request):
    """
    Employee Directory View:
    Displays all employees with live search (name or email) and department filtering.
    """
    search_query = request.GET.get('q', '').strip()
    selected_dept = request.GET.get('department', '').strip()

    employees = Employee.objects.all()

    if search_query:
        employees = employees.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if selected_dept:
        employees = employees.filter(department=selected_dept)

    # Pagination: 10 employees per page
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'employees': page_obj.object_list,
        'search_query': search_query,
        'selected_dept': selected_dept,
        'department_choices': Employee.DEPARTMENT_CHOICES,
        'total_filtered_count': employees.count(),
    }
    return render(request, 'employees/employee_list.html', context)


def employee_detail(request, pk):
    """
    Employee Detail View:
    Displays comprehensive profile details of an individual employee.
    """
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


def employee_create(request):
    """
    Add Employee View:
    Handles registration form display, input validation, and saving to MySQL.
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(
                request,
                f'Employee "{employee.full_name}" (ID #{employee.id}) was successfully registered!'
            )
            return redirect('employees:employee_list')
        else:
            messages.error(request, 'Please correct the errors in the form below.')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add New Employee',
        'is_edit': False,
    })


def employee_update(request, pk):
    """
    Edit Employee View:
    Retrieves existing employee by database ID, presents pre-filled form,
    validates modifications, and persists updates to MySQL.
    """
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            updated_employee = form.save()
            messages.success(
                request,
                f'Employee "{updated_employee.full_name}" was successfully updated!'
            )
            return redirect('employees:employee_list')
        else:
            messages.error(request, 'Please correct the errors in the form below.')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'employee': employee,
        'title': f'Edit Employee: {employee.full_name}',
        'is_edit': True,
    })


def employee_delete(request, pk):
    """
    Delete Employee View:
    Displays confirmation page before deletion.
    Executes deletion only on POST request for CSRF safety.
    """
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        name = employee.full_name
        employee.delete()
        messages.success(request, f'Employee "{name}" has been permanently removed from the system.')
        return redirect('employees:employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

