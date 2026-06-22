# 🏢 Avangard HRM API

> A REST API system for HR and business process management with role-based access control

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16-red)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange)](https://jwt.io)
[![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL-blue?logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 About

**Avangard HRM API** is a backend system for managing employees, tasks, finances, and company metrics. Built with Django REST Framework, JWT authentication, and a three-level role-based access model.

Key features:
- Employee management with role assignments
- Task and workflow tracking
- Financial records and reporting
- Metrics collection and analytics
- Action logging
- Role-based access control (Admin / Boss / Operator)

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12 | Language |
| Django | 5.2 | Web framework |
| Django REST Framework | 3.16 | REST API |
| SimpleJWT | 5.5 | JWT authentication |
| drf-spectacular | 0.29 | OpenAPI / Swagger docs |
| PostgreSQL | — | Database |
| psycopg2 | 2.9 | PostgreSQL driver |
| openpyxl | 3.1 | Excel export |
| whitenoise | 6.11 | Static file serving |
| python-dotenv | 1.2 | Environment configuration |
| Docker | — | Containerization |

---

## 📁 Project Structure

```
avangard/
├── config/          # Django settings, urls, wsgi, asgi
├── users/           # Custom user model, authentication, roles
├── employees/       # Employee management
├── work/            # Tasks and workflows
├── finance/         # Financial module
├── metrics/         # Metrics and analytics
├── logs/            # Action logging
├── manage.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## 🔐 Roles & Permissions

| Role | Description |
|---|---|
| **Admin** | Full access to all system resources |
| **Boss** | Employee management and metrics viewing |
| **Operator** | Task operations and basic access |

Authentication via **JWT tokens** (access + refresh). All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Defa13/Avangard_CS.git
cd Avangard_CS
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Fill in the variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/avangard
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

---

## 📖 API Documentation

Once running, the docs are available at:

| Interface | URL |
|---|---|
| **Swagger UI** | http://127.0.0.1:8000/docs/ |
| **ReDoc** | http://127.0.0.1:8000/redoc/ |
| **Admin panel** | http://127.0.0.1:8000/admin/ |

---

## 🐳 Docker

```bash
docker build -t avangard-api .
docker run -p 8000:8000 --env-file .env avangard-api
```

---

## 📡 API Endpoints

### Authentication
```
POST /users/login/        — obtain JWT tokens
POST /users/logout/       — logout (invalidate refresh token)
```

### Users
```
GET    /users/users/         — list users
POST   /users/users/         — create user
GET    /users/users/{id}/    — retrieve user
PUT    /users/users/{id}/    — update user
DELETE /users/users/{id}/    — delete user
```

### Employees, Tasks, Finance
```
/employees/...   — employee management
/work/...        — tasks and workflows
/finance/...     — financial records
/metrics/...     — analytics and metrics
/logs/...        — action logs
```

> Full docs with all parameters and request schemas available in Swagger UI

---

## 🤝 Contact

**GitHub:** [Defa13](https://github.com/Defa13)
