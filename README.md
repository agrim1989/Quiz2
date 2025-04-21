# Employee Management System

A Django REST API-based employee management system with data generation, visualization, and analytics capabilities.

## Features

- Synthetic employee data generation
- PostgreSQL database integration
- REST API endpoints for data access
- Interactive data visualization
- JWT Authentication
- Rate limiting
- Swagger UI documentation

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

5. Set up the database:
```bash
python manage.py migrate
```

6. Generate sample data:
```bash
python manage.py generate_sample_data
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

Access the Swagger UI documentation at:
```
http://localhost:8000/swagger/
```

## Available Endpoints

- `/api/auth/` - Authentication endpoints
- `/api/employees/` - Employee management
- `/api/attendance/` - Attendance records
- `/api/performance/` - Performance metrics
- `/api/analytics/` - Data analytics and visualization

## Rate Limiting

API endpoints are rate-limited to prevent abuse. Default limits:
- 100 requests per hour for authenticated users
- 20 requests per hour for anonymous users

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:
1. Obtain a token from `/api/auth/token/`
2. Include the token in the Authorization header: `Bearer <token>` 