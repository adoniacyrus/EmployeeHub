# ==============================================================================
# EmployeeHub - Production-Grade Academic Dockerfile
# Python 3.11-slim + MySQL Client Dependencies + Django 5 Application
# ==============================================================================

FROM python:3.11-slim

# Prevent Python from writing bytecode (.pyc) and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system runtime & compilation dependencies for mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    default-mysql-client \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script and ensure executable permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy Django application directory
COPY employeehub /app/employeehub

WORKDIR /app/employeehub

# Expose web server port
EXPOSE 8000

# Use startup entrypoint to wait for MySQL and execute migrations
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

