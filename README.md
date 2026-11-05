# EmployeeHub – Employee Management System

> **Course:** 24MCAT203 – Virtualisation and Containers  
> **Degree Program:** Master of Computer Applications (MCA)  
> **Project Type:** Academic Microproject  
> **Technologies:** Python Django, MySQL 8, Docker & Docker Compose, Bootstrap 5  

---

## 1. Abstract

**EmployeeHub** is a production-grade, containerized Employee Management System engineered for enterprise workforce record keeping. Designed as an academic microproject for the MCA curriculum in *Virtualisation and Containers*, the system demonstrates the practical implementation of full Create, Read, Update, and Delete (CRUD) operations backed by an enterprise relational database (MySQL 8) and an industry-standard web framework (Python Django). The entire architecture is decoupled, containerized, and orchestrated using Docker and Docker Compose, achieving isolated service runtimes, declarative networking, and persistent data storage across container lifecycles.

---

## 2. Introduction

Modern enterprise software architecture has shifted decisively from monolithic, host-dependent runtimes toward lightweight, containerized micro-architectures. In conventional development environments, challenges such as "it works on my machine", operating system dependency mismatches, and database driver discrepancies frequently disrupt software deployment.

EmployeeHub addresses these challenges by encapsulating:
1. The **Application Tier** (Python 3.11, Django 5, Gunicorn/WSGI, Bootstrap 5 frontend) inside an application container (`web`).
2. The **Database Tier** (MySQL 8 InnoDB engine) inside a dedicated database service container (`db`).
3. Declarative **Container Networking** and **Named Volumes** to guarantee fault-tolerant persistence and secure inter-service communication.

---

## 3. Objectives

- **Practical Virtualization & Containerization:** Demonstrate container lifecycle management, custom Docker image authoring, multi-stage health checking, and multi-container orchestration.
- **Full CRUD Implementation:** Deliver robust Create, Read, Update, and Delete interfaces for employee management.
- **Decoupled Architecture:** Separate web runtime and database servers into independent containers communicating over a user-defined bridge network.
- **Stateful Data Persistence:** Ensure persistent database storage that outlives container termination, restarts, and image updates using Docker named volumes.
- **Enterprise-Grade Clean Code:** Eliminate hardcoded credentials using environment variable injection (`.env`), follow Django MVC/MVT patterns, and deliver a responsive Bootstrap 5 user dashboard.

---

## 4. Technology Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript | Modern Standards | Semantic structure, dynamic UI interactivity |
| **UI Framework** | Bootstrap 5 & Bootstrap Icons | 5.3.3 / 1.11.3 | Responsive grid, form components, stat cards |
| **Typography** | Inter Font Family | Variable Google Font | Clean, professional dashboard typography |
| **Backend Framework** | Python Django | 5.0.x / 5.1.x | MVC/MVT web architecture, ORM, URL routing, forms |
| **Database Engine** | MySQL Community Server | 8.0 | ACID-compliant relational persistence, InnoDB engine |
| **Database Client** | `mysqlclient` (C-connector) | 2.2.x | High-performance Python-to-MySQL communication |
| **Container Engine** | Docker Community / Desktop | 29.x / Engine v27+ | Operating-system-level virtualization |
| **Orchestrator** | Docker Compose | Specification v2 / v5 | Declarative multi-container orchestration |

---

## 5. Functional Requirements

### 1. Dashboard (Overview & Analytics)
- Real-time aggregation of **Total Employees** from the MySQL database.
- Dynamic count of **Active Departments**.
- Dynamic count and listing of **Recently Added Employees** (latest 5 registrations).
- Visual distribution breakdown showing employee allocations per department.
- Quick action navigation to add new staff or view the directory.

### 2. Employee Directory (Read & Search)
- Tabular display of: Employee ID, Full Name, Email, Phone, Department, Designation, Date of Joining, and Actions.
- Real-time case-insensitive search by **Full Name** or **Email Address**.
- Dropdown filtering by **Department** (`IT`, `HR`, `Finance`, `Marketing`, `Sales`, `Operations`).
- Responsive pagination (10 employees per page).
- Empty state indicator when no records match filter criteria.

### 3. Employee Registration (Create)
- Form inputs: Full Name, Email, Phone, Gender, Department, Designation, Date of Joining, Monthly Salary, Residential Address.
- Server-side email uniqueness validation (prevents duplicate entries).
- Positive salary validation ($> 0$).
- Contact phone formatting and length validation.
- Success notifications via Django messages framework.

### 4. Employee Modification (Update)
- Retrieval of selected employee by primary key (`id`).
- Pre-population of existing data into the form.
- Field-level validation upon submission.
- Update persistence into MySQL with immediate redirect and feedback.

### 5. Employee Removal (Delete)
- Confirmation interstitial displaying the target employee's details and warning.
- Safe execution using HTTP `POST` requests protected by Django CSRF tokens.
- Permanent record deletion and success notification.

---

## 6. System Architecture

```
                                  +--------------------------------------------------+
                                  |                 HOST WORKSTATION                 |
                                  |             (Browser: localhost:8000)            |
                                  +------------------------+-------------------------+
                                                           |
                                                           | Port Mapping 8000:8000
                                                           v
+--------------------------------------------------------------------------------------------------------+
|                                  DOCKER BRIDGE NETWORK (employeehub_network)                          |
|                                                                                                        |
|   +---------------------------------------------+      +-------------------------------------------+   |
|   |             SERVICE: web                    |      |                SERVICE: db                |   |
|   |         (employeehub_web)                   |      |           (employeehub_db)                |   |
|   |                                             |      |                                           |   |
|   |  - Base: python:3.11-slim                   |      |  - Image: mysql:8.0                       |   |
|   |  - Framework: Django 5                      |      |  - Engine: InnoDB (utf8mb4)               |   |
|   |  - Static & Templates Engine                |      |  - Database: employeehub_db               |   |
|   |  - Environment: .env                        |      |  - Healthcheck: mysqladmin ping           |   |
|   |  - Entrypoint: wait for DB -> migrate -> run|      |  - Port inside network: 3306              |   |
|   |                                             |      |  - Host port exposed: 3307                |   |
|   +----------------------+----------------------+      +---------------------+---------------------+   |
|                          |                                                   |                         |
|                          +----------------- TCP (DB_HOST=db) ----------------+                         |
|                                                  Port 3306                                             |
+--------------------------------------------------------------------------------------------------------+
                                                                               |
                                                                               | Mounts /var/lib/mysql
                                                                               v
                                                         +-------------------------------------------+
                                                         |             NAMED DOCKER VOLUME           |
                                                         |          (employeehub_mysql_data)         |
                                                         |  - Persistent storage across restarts     |
                                                         +-------------------------------------------+
```

---

## 7. Database Design

### Table: `employees_employee`

| Column | Data Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | `BIGINT` | `AUTO_INCREMENT`, `PRIMARY KEY` | Unique employee identifier |
| `full_name` | `VARCHAR(150)` | `NOT NULL` | Employee full name |
| `email` | `VARCHAR(254)` | `NOT NULL`, `UNIQUE` | Unique email address |
| `phone` | `VARCHAR(20)` | `NOT NULL`, Regex-validated | Contact telephone number |
| `gender` | `VARCHAR(10)` | `NOT NULL`, Choice (`Male`/`Female`/`Other`) | Gender designation |
| `department` | `VARCHAR(50)` | `NOT NULL`, Choice (`IT`/`HR`/`Finance`...) | Assigned department |
| `designation` | `VARCHAR(100)` | `NOT NULL` | Job role / designation |
| `joining_date` | `DATE` | `NOT NULL` | Employment start date |
| `salary` | `DECIMAL(10,2)` | `NOT NULL`, Min: 0.01 | Monthly compensation |
| `address` | `LONGTEXT` | `NULLABLE` | Residential address |
| `created_at` | `DATETIME(6)` | `NOT NULL`, Auto-generated | Record creation timestamp |

---

## 8. Project Folder Structure

```
EmployeeHub/
│
├── employeehub/                       # Django Project Root
│   ├── manage.py                     # Django administrative entry script
│   │
│   ├── config/                       # Project Configuration Package
│   │   ├── __init__.py
│   │   ├── settings.py               # Settings configured with .env & MySQL backend
│   │   ├── urls.py                   # Global routing definitions
│   │   ├── wsgi.py                   # WSGI deployment entry point
│   │   └── asgi.py                   # ASGI asynchronous entry point
│   │
│   ├── employees/                    # Core Business Logic Application
│   │   ├── migrations/               # Database versioned migration scripts
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py       # Initial schema creation for Employee model
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django Admin model registration & filters
│   │   ├── apps.py                   # App configuration class
│   │   ├── forms.py                  # ModelForm with validation & Bootstrap widgets
│   │   ├── models.py                 # Employee model definition
│   │   ├── tests.py                  # Automated unit test suite (CRUD operations)
│   │   ├── urls.py                   # App-specific URL routes
│   │   └── views.py                  # View functions (Dashboard, CRUD, Search)
│   │
│   ├── templates/                    # HTML5 Templates (Bootstrap 5)
│   │   ├── base.html                 # Master layout (sidebar, navbar, footer)
│   │   └── employees/
│   │       ├── dashboard.html        # Analytics dashboard with dynamic metric cards
│   │       ├── employee_list.html    # Directory table with search, filter, pagination
│   │       ├── employee_detail.html  # Comprehensive employee profile view
│   │       ├── employee_form.html    # Add/Edit employee registration form
│   │       └── employee_confirm_delete.html # Confirmation modal for deletion
│   │
│   └── static/                       # Static Assets
│       ├── css/
│       │   └── style.css             # Custom modern styling
│       └── js/
│           └── main.js               # Sidebar toggle & alert dismissal scripts
│
├── Dockerfile                        # Multi-layer Docker build definition
├── docker-compose.yml                # Multi-service container orchestration
├── entrypoint.sh                     # Automated DB wait & migration shell script
├── requirements.txt                  # Python package dependencies
├── .env                              # Active local environment variables
├── .env.example                      # Safe template environment variables
├── .dockerignore                     # Build context exclusion rules
└── README.md                         # Comprehensive academic project documentation
```

---

## 9. Understanding Docker Concepts (MCA Academic Guide)

During a practical examination or project viva, you may be asked to explain each containerization component. Here is how they work in EmployeeHub:

### 1. What is a Dockerfile?
A `Dockerfile` is a declarative text recipe containing step-by-step instructions to assemble a Docker image.
- `FROM python:3.11-slim`: Pulls a minimal, secure Linux base image with Python 3.11 pre-installed.
- `RUN apt-get update && apt-get install`: Installs C compilers and MySQL development client libraries (`default-libmysqlclient-dev`) needed by `mysqlclient`.
- `COPY requirements.txt . && RUN pip install`: Installs the required Python libraries.
- `ENTRYPOINT ["/app/entrypoint.sh"]`: Ensures that whenever the container starts, it automatically polls MySQL until it is healthy, runs `python manage.py migrate`, and then starts the Django server.

### 2. What is a Docker Image vs. Container?
- **Docker Image:** A read-only, immutable snapshot template containing the operating system, runtime libraries, application code, and dependencies.
- **Docker Container:** A running, isolated instance of an image. If an image is a "class", a container is an instantiated "object".

### 3. What is Docker Compose?
`docker-compose.yml` is an orchestration specification that coordinates multiple containers. Instead of typing complex, lengthy `docker run` commands with dozens of arguments, Docker Compose allows you to spin up the entire application stack (`web` + `db` + networking + volumes) with a single command:
```bash
docker compose up --build
```

### 4. Docker Networking (Inter-Service Communication)
Docker creates a private virtual network (`employeehub_network`). Containers on this network resolve each other by **service name** via Docker's embedded DNS:
- The Django container connects to MySQL using `DB_HOST=db`, **NOT** `localhost`.
- Inside the Docker network, `localhost` refers only to the container itself. Using `DB_HOST=db` directs traffic to the IP address assigned to the `db` container.

### 5. Docker Volumes (Data Persistence)
Containers are stateless and ephemeral by default: if a container is removed, data written inside its root filesystem is deleted.
To prevent database loss, a named volume (`employeehub_mysql_data`) is mapped to MySQL's storage directory (`/var/lib/mysql`). When the database writes tables and records, they are safely persisted on the host machine. Even if you run `docker compose down`, your employee records remain safe inside the named volume.

---

## 10. Installation and Execution Guide

### Prerequisites
1. **Docker Desktop** installed on Windows, macOS, or Linux.
2. Docker Engine running with WSL2 backend (on Windows).
3. Port `8000` (for Django web) and Port `3307` (for MySQL host exposure) free on your machine.

### Quick Start (One Command)

Open your terminal (PowerShell, Command Prompt, or bash) in the project directory:

```bash
# Navigate to EmployeeHub
cd EmployeeHub

# Build and start all services in detached mode
docker compose up --build -d
```

Once the build finishes, open your browser and navigate to:
```
http://localhost:8000
```

---

## 11. Essential Docker Commands for the Practical Viva

### 1. View Running Containers
Verify that both `employeehub_web` and `employeehub_db` are running:
```bash
docker ps
```

### 2. View Real-time Application Logs
Inspect startup logs, migrations, and HTTP requests:
```bash
docker compose logs -f
# Or inspect web logs specifically:
docker compose logs -f web
```

### 3. Stop Containers Gracefully
Stop the containers without removing them:
```bash
docker compose stop
```

### 4. Stop and Remove Containers (Data Preserved)
Stop and tear down the containers and network (named volume is retained):
```bash
docker compose down
```

### 5. Inspect Named Volumes
Verify the persistent MySQL volume:
```bash
docker volume ls
```

### 6. Inspect Virtual Networks
Verify the bridge network:
```bash
docker network ls
```

### 7. Open an Interactive Shell inside the Django Web Container
```bash
docker compose exec web bash
```

### 8. Access the MySQL Database Directly via Terminal
Execute SQL queries directly inside the database container:
```bash
docker compose exec db mysql -u employee_user -pemployee_pass123 employeehub_db
```
Inside the MySQL shell, inspect the table:
```sql
SHOW TABLES;
SELECT id, full_name, email, department, designation, salary FROM employees_employee;
EXIT;
```

---

## 12. Testing Procedure & Verification

### Running Automated Django Tests inside Docker
EmployeeHub includes comprehensive automated unit tests covering all CRUD operations, duplicate validations, search, filtering, and dashboard stats:

```bash
docker compose exec web python manage.py test employees
```

**Expected Result:**
```
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 0.420s

OK
Destroying test database for alias 'default'...
```

### Manual CRUD Verification Checklist

| Test Case | Procedure | Expected Output | Status |
| :--- | :--- | :--- | :--- |
| **1. Create** | Click "+ Add Employee", submit valid data | Record saved in MySQL, redirected to Directory with green banner | Verified |
| **2. Read** | Open Dashboard & Directory | Correct statistics, employee card rendered with accurate details | Verified |
| **3. Update** | Click edit on an employee, update designation and salary | Changes reflected in database and updated on profile | Verified |
| **4. Delete** | Click delete, view confirmation page, click "Confirm Delete" | Record permanently deleted from MySQL, success message displayed | Verified |
| **5. Validation** | Submit an existing email or negative salary | Red inline validation error messages appear, form refuses save | Verified |
| **6. Search** | Type employee name in search bar | Table dynamically filters matching records | Verified |
| **7. Filter** | Select department from dropdown | Table shows only employees from that department | Verified |
| **8. Persistence** | Add employees -> `docker compose down` -> `docker compose up -d` | All previously entered employee records remain intact | Verified |

---

## 13. Data Persistence Proof Demonstration

To demonstrate Docker persistence during your evaluation:

1. Start containers and add 2–3 employees via `http://localhost:8000`.
2. Stop and remove the containers:
   ```bash
   docker compose down
   ```
3. Verify containers are removed:
   ```bash
   docker ps -a
   ```
4. Verify the volume still exists:
   ```bash
   docker volume ls | grep employeehub
   ```
5. Re-launch the containers:
   ```bash
   docker compose up -d
   ```
6. Refresh `http://localhost:8000`. All previously added employee records are completely preserved!

---

## 14. Conclusion

The **EmployeeHub** project successfully demonstrates the synergy between Python Django, MySQL 8, and modern containerization technologies. By separating application logic from database persistence and encapsulating dependencies within Docker images, the project achieves environment parity, zero-configuration portability, and robust data persistence. This microproject fulfills all syllabus objectives for MCA 24MCAT203 (*Virtualisation and Containers*).

