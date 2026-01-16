# Employee Management API

A RESTful API for managing employee records with authentication, built with Django REST Framework.

## Overview

This project implements a complete CRUD (Create, Read, Update, Delete) API for employee management. It includes token-based authentication, filtering, pagination, and comprehensive error handling.

## Features

- Full CRUD operations for employee management
- JWT token-based authentication
- Email validation and uniqueness constraints
- Filtering by department and role
- Pagination support (10 items per page)
- Comprehensive error handling
- Unit tests for all endpoints
- Clean, modular code structure

## Tech Stack

- Python 3.8+
- Django 4.2+
- Django REST Framework
- SQLite (default database)

## Installation & Setup

### 1. Clone the Repository

git clone <your-repository-url>
cd employee_api

### 2. Create Virtual Environment

# On Windows
python -m venv venv
venv\\Scripts\\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run Migrations

python manage.py makemigrations
python manage.py migrate

### 5. Create Superuser

python manage.py createsuperuser

### 6. Run the Development Server

python manage.py runserver

The API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## API Documentation

### Authentication

All employee endpoints require authentication. First, obtain a token:

**Endpoint:** POST /api/auth/register/

**Request Body:**
{
  "username": "testuser",
  "password": "testpass123",
  "email": "test@example.com"
}

**Response:**
{
  "token": "your-jwt-token-here",
  "user_id": 1,
  "username": "testuser"
}

### Employee Endpoints

All requests require the Authorization header:
Authorization: Token <your-token>

#### 1. Create Employee
- POST /api/employees/
- Body: {"name": "John Doe", "email": "john@example.com", "department": "Engineering", "role": "Developer"}
- Response: 201 Created

#### 2. List All Employees
- GET /api/employees/
- Query Parameters: page=1, department=Engineering, role=Developer
- Response: 200 OK

#### 3. Retrieve Single Employee
- GET /api/employees/{id}/
- Response: 200 OK or 404 Not Found

#### 4. Update Employee
- PUT /api/employees/{id}/
- Body: {"name": "John Updated", "email": "john@example.com", "department": "HR", "role": "Manager"}
- Response: 200 OK

#### 5. Delete Employee
- DELETE /api/employees/{id}/
- Response: 204 No Content

## Running Tests

python manage.py test

## Error Handling

The API returns appropriate HTTP status codes:
- 200 OK - Successful GET/PUT request
- 201 Created - Successful POST request
- 204 No Content - Successful DELETE request
- 400 Bad Request - Validation errors
- 401 Unauthorized - Missing or invalid authentication
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server errors
