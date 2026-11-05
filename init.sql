-- Grant privileges for employee_user to create test databases during test runs
GRANT ALL PRIVILEGES ON *.* TO 'employee_user'@'%';
FLUSH PRIVILEGES;

