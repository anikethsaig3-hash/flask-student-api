# Flask Student API - Comprehensive Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [API Endpoints](#api-endpoints)
5. [Authentication](#authentication)
6. [Error Handling](#error-handling)
7. [Validation Rules](#validation-rules)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## Overview

**Flask Student API** is a production-ready REST API for managing student records. It provides comprehensive CRUD operations with advanced filtering, searching, pagination, and statistics capabilities.

### Key Features
- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ Advanced filtering and search
- ✅ Pagination support
- ✅ Input validation and error handling
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Statistics and analytics
- ✅ Comprehensive unit tests
- ✅ Postman collection included

### Technology Stack
- **Framework**: Flask 2.3.2
- **ORM**: SQLAlchemy 2.0.19
- **Database**: SQLite
- **Testing**: Python unittest
- **Documentation**: OpenAPI/Swagger compatible

---

## Architecture

### Project Structure
```
flask-student-api/
├── app.py                      # Flask application factory
├── models.py                   # Database models & validation
├── routes.py                   # API endpoints (CRUD)
├── config.py                   # Configuration management
├── seed.py                     # Database seeding script
├── test_api.py                 # Unit tests
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── Flask_Student_API.postman_collection.json  # Postman collection
├── API_DOCUMENTATION.md        # This file
└── README.md                   # Project README
```

### Design Pattern
The API follows the **Factory Pattern** for Flask app initialization and **Blueprint Pattern** for route organization.

```
Request → Flask App → Blueprint Routes → Models → Database
                  ↓
            Error Handlers
                  ↓
            JSON Response
```

### Database Schema

```
Students Table
├── id (Integer, Primary Key, Auto-increment)
├── name (String[100], Required, Indexed)
├── department (String[50], Required)
├── cgpa (Float, Required, Range: 0.0-4.0)
├── email (String[120], Required, Unique, Indexed)
├── created_at (DateTime, Auto-populated)
└── updated_at (DateTime, Auto-updated on modification)
```

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment tool

### Step-by-Step Setup

#### 1. Clone Repository
```bash
git clone https://github.com/anikethsaig3-hash/flask-student-api.git
cd flask-student-api
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env if needed (already configured for development)
```

#### 5. Initialize Database
```bash
# The database is auto-created on first run
# But you can seed it with sample data:
python seed.py
```

#### 6. Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

#### 7. Verify Installation
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "success": true,
  "message": "API is running",
  "status": "healthy"
}
```

---

## API Endpoints

### Base URL
```
http://localhost:5000/api/students
```

### 1. Health Check
**Endpoint**: `GET /health`

Check if the API is running.

**Response**:
```json
{
  "success": true,
  "message": "API is running",
  "status": "healthy"
}
```

---

### 2. Create Student
**Endpoint**: `POST /api/students`

Create a new student record.

**Request Body**:
```json
{
  "name": "Alice Brown",
  "department": "Computer Science",
  "cgpa": 3.75,
  "email": "alice.brown@university.edu"
}
```

**Success Response (201)**:
```json
{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 13,
    "name": "Alice Brown",
    "department": "Computer Science",
    "cgpa": 3.75,
    "email": "alice.brown@university.edu",
    "created_at": "2024-01-20T10:30:45",
    "updated_at": "2024-01-20T10:30:45"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Missing required fields or invalid data
- `409 Conflict`: Email already exists

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Brown",
    "department": "Computer Science",
    "cgpa": 3.75,
    "email": "alice.brown@university.edu"
  }'
```

---

### 3. Get All Students
**Endpoint**: `GET /api/students`

Retrieve all students with optional filtering, searching, sorting, and pagination.

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number for pagination |
| per_page | integer | 10 | Items per page (max: 100) |
| department | string | - | Filter by department |
| min_cgpa | float | - | Minimum CGPA (0.0-4.0) |
| max_cgpa | float | - | Maximum CGPA (0.0-4.0) |
| search | string | - | Search by name or email |
| sort_by | string | created_at | Sort field (id, name, department, cgpa, email, created_at, updated_at) |
| sort_order | string | desc | Sort order (asc, desc) |

**Response (200)**:
```json
{
  "success": true,
  "message": "Students retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "department": "Computer Science",
      "cgpa": 3.8,
      "email": "john.doe@university.edu",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "department": "Electronics",
      "cgpa": 3.9,
      "email": "jane.smith@university.edu",
      "created_at": "2024-01-15T10:31:00",
      "updated_at": "2024-01-15T10:31:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 2,
    "total_pages": 1
  }
}
```

**Examples**:

Get first 5 students:
```bash
curl http://localhost:5000/api/students?page=1&per_page=5
```

Filter by department:
```bash
curl "http://localhost:5000/api/students?department=Computer%20Science"
```

Filter by CGPA range:
```bash
curl "http://localhost:5000/api/students?min_cgpa=3.7&max_cgpa=4.0"
```

Search by name:
```bash
curl "http://localhost:5000/api/students?search=john"
```

Sort by CGPA (descending):
```bash
curl "http://localhost:5000/api/students?sort_by=cgpa&sort_order=desc"
```

Combined filters:
```bash
curl "http://localhost:5000/api/students?department=Computer%20Science&min_cgpa=3.5&sort_by=cgpa&sort_order=desc"
```

---

### 4. Get Single Student
**Endpoint**: `GET /api/students/{id}`

Retrieve a specific student by ID.

**URL Parameters**:
- `id` (required): Student ID

**Response (200)**:
```json
{
  "success": true,
  "message": "Student retrieved successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "department": "Computer Science",
    "cgpa": 3.8,
    "email": "john.doe@university.edu",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**Error Response (404)**:
```json
{
  "success": false,
  "message": "Student with ID 999 not found"
}
```

**cURL Example**:
```bash
curl http://localhost:5000/api/students/1
```

---

### 5. Update Student
**Endpoint**: `PUT /api/students/{id}`

Update a student record. Supports partial updates.

**URL Parameters**:
- `id` (required): Student ID

**Request Body** (all fields optional):
```json
{
  "name": "John Updated",
  "department": "Electronics",
  "cgpa": 3.9,
  "email": "john.updated@university.edu"
}
```

**Response (200)**:
```json
{
  "success": true,
  "message": "Student updated successfully",
  "data": {
    "id": 1,
    "name": "John Updated",
    "department": "Electronics",
    "cgpa": 3.9,
    "email": "john.updated@university.edu",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-20T15:45:30"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid data format
- `404 Not Found`: Student not found
- `409 Conflict`: Email already in use

**cURL Example**:
```bash
curl -X PUT http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "cgpa": 3.9,
    "department": "Electronics"
  }'
```

---

### 6. Delete Student
**Endpoint**: `DELETE /api/students/{id}`

Delete a student record.

**URL Parameters**:
- `id` (required): Student ID

**Response (200)**:
```json
{
  "success": true,
  "message": "Student deleted successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "department": "Computer Science",
    "cgpa": 3.8,
    "email": "john.doe@university.edu",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**Error Response (404)**:
```json
{
  "success": false,
  "message": "Student with ID 999 not found"
}
```

**cURL Example**:
```bash
curl -X DELETE http://localhost:5000/api/students/1
```

---

### 7. Get Statistics
**Endpoint**: `GET /api/students/stats/summary`

Retrieve statistics about all students.

**Response (200)**:
```json
{
  "success": true,
  "message": "Statistics retrieved successfully",
  "data": {
    "total_students": 12,
    "average_cgpa": 3.68,
    "highest_cgpa": 3.9,
    "lowest_cgpa": 3.3,
    "departments": {
      "Computer Science": 4,
      "Electronics": 2,
      "Mechanical": 2,
      "Civil": 2,
      "Electrical": 2
    }
  }
}
```

**cURL Example**:
```bash
curl http://localhost:5000/api/students/stats/summary
```

---

## Authentication

Currently, the API does **not** require authentication. All endpoints are publicly accessible.

### Future Enhancement
For production deployment, implement JWT or API key authentication:

```python
from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        # Validate token
        return f(*args, **kwargs)
    return decorated

@app.route('/api/students', methods=['GET'])
@token_required
def get_students():
    # Implementation
    pass
```

---

## Error Handling

The API returns consistent error responses with appropriate HTTP status codes.

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request successful |
| 201 | Created | Student created successfully |
| 400 | Bad Request | Invalid input or missing fields |
| 404 | Not Found | Student not found |
| 405 | Method Not Allowed | Wrong HTTP method used |
| 409 | Conflict | Duplicate email or constraint violation |
| 500 | Internal Server Error | Server error |

### Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "message": "Human-readable error message",
  "error": "Optional detailed error information"
}
```

### Common Errors

#### Missing Required Fields (400)
```json
{
  "success": false,
  "message": "Missing required fields: department, cgpa, email"
}
```

#### Invalid Email Format (400)
```json
{
  "success": false,
  "message": "Invalid email format"
}
```

#### CGPA Out of Range (400)
```json
{
  "success": false,
  "message": "CGPA must be a number between 0.0 and 4.0"
}
```

#### Duplicate Email (409)
```json
{
  "success": false,
  "message": "Student with email john.doe@university.edu already exists"
}
```

#### Student Not Found (404)
```json
{
  "success": false,
  "message": "Student with ID 999 not found"
}
```

---

## Validation Rules

### Name
- **Type**: String
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 100 characters
- **Validation**: `^.{1,100}$`

### Department
- **Type**: String
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 50 characters
- **Validation**: `^.{1,50}$`

### CGPA
- **Type**: Float
- **Required**: Yes
- **Min Value**: 0.0
- **Max Value**: 4.0
- **Validation**: `0.0 <= cgpa <= 4.0`

### Email
- **Type**: String
- **Required**: Yes
- **Unique**: Yes (no duplicates allowed)
- **Format**: Standard email format
- **Validation**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

### Validation Examples

Valid:
```json
{
  "name": "John Doe",
  "department": "Computer Science",
  "cgpa": 3.8,
  "email": "john@example.com"
}
```

Invalid (CGPA out of range):
```json
{
  "name": "John Doe",
  "department": "Computer Science",
  "cgpa": 4.5,
  "email": "john@example.com"
}
```

Invalid (Bad email):
```json
{
  "name": "John Doe",
  "department": "Computer Science",
  "cgpa": 3.8,
  "email": "invalid-email"
}
```

---

## Testing

### Running Tests

#### Run all tests
```bash
python -m unittest test_api.py -v
```

#### Run specific test class
```bash
python -m unittest test_api.StudentAPITestCase -v
```

#### Run specific test
```bash
python -m unittest test_api.StudentAPITestCase.test_create_student_success -v
```

### Test Coverage

The test suite includes 40+ test cases covering:

- **Health Check**: 1 test
- **Create Operations**: 7 tests
- **Read Operations**: 10 tests
- **Update Operations**: 5 tests
- **Delete Operations**: 2 tests
- **Statistics**: 3 tests
- **Validation**: 3 tests
- **Edge Cases**: 3 tests
- **Total**: 40+ tests

### Test Categories

#### 1. CRUD Operations
```bash
test_create_student_success
test_get_all_students
test_get_single_student
test_update_student_success
test_delete_student_success
```

#### 2. Validation Tests
```bash
test_create_student_invalid_email
test_create_student_invalid_cgpa
test_create_student_empty_name
test_validate_name_length
test_validate_department_length
```

#### 3. Error Handling
```bash
test_create_student_missing_fields
test_create_student_duplicate_email
test_get_student_not_found
test_update_student_not_found
test_delete_student_not_found
```

#### 4. Filtering & Searching
```bash
test_get_all_students_filter_by_department
test_get_all_students_filter_by_cgpa_range
test_get_all_students_search_by_name
test_get_all_students_search_by_email
```

#### 5. Sorting & Pagination
```bash
test_get_all_students_sort_by_cgpa_desc
test_get_all_students_sort_by_name_asc
test_get_all_students_pagination
test_get_all_students_combined_filters
```

### Running Tests with Coverage

```bash
pip install coverage
coverage run -m unittest test_api.py
coverage report
coverage html
```

---

## Deployment

### Development Environment
```bash
python app.py
# Runs on http://localhost:5000 with debug mode enabled
```

### Production Environment

#### Using Gunicorn

```bash
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With custom settings
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 60 --access-logfile - app:app
```

#### Using Docker

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Build and run**:
```bash
docker build -t flask-student-api .
docker run -p 5000:5000 flask-student-api
```

#### Deployment Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode
- [ ] Use strong database backups
- [ ] Implement rate limiting
- [ ] Add CORS headers if needed
- [ ] Use HTTPS/SSL certificate
- [ ] Set up monitoring and logging
- [ ] Configure firewalls
- [ ] Implement authentication
- [ ] Set up CI/CD pipeline

---

## Troubleshooting

### Issue: Database file not created

**Solution**:
```bash
# Ensure the app creates the database
python -c "from app import create_app; app = create_app(); app.app_context().push()"
```

### Issue: Port 5000 already in use

**Solution**:
```bash
# Use a different port
python app.py --port 5001

# Or kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

### Issue: Import errors

**Solution**:
```bash
# Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Issue: Tests failing

**Solution**:
```bash
# Clear database and reseed
python seed.py

# Run tests with verbose output
python -m unittest test_api.py -v
```

### Issue: Invalid CGPA error

**Solution**:
Ensure CGPA is between 0.0 and 4.0:
```json
{
  "cgpa": 3.5  // Valid
}
```

---

## Performance Optimization

### Database Indexing
The API uses indexes on:
- `id` (Primary key)
- `email` (Unique, frequently searched)
- `name` (Frequently searched)

### Query Optimization
- Pagination limits to prevent loading too much data
- Efficient filtering with SQLAlchemy ORM
- Database-level sorting

### Caching Opportunities
Future enhancements:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/students/stats/summary')
@cache.cached(timeout=300)
def get_statistics():
    # Cached for 5 minutes
    pass
```

---

## API Versioning

For future versions, implement versioning:

```python
# app.py
student_bp_v1 = Blueprint('students_v1', __name__, url_prefix='/api/v1/students')
app.register_blueprint(student_bp_v1)
```

---

## Changelog

### Version 1.0.0 (Initial Release)
- ✅ Full CRUD operations
- ✅ Filtering and searching
- ✅ Pagination
- ✅ Statistics endpoint
- ✅ Comprehensive unit tests
- ✅ Postman collection
- ✅ Complete documentation

---

## Support & Contributing

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Support
For issues and questions, please create a GitHub issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Glossary

- **CRUD**: Create, Read, Update, Delete
- **API**: Application Programming Interface
- **REST**: Representational State Transfer
- **JSON**: JavaScript Object Notation
- **ORM**: Object-Relational Mapping
- **CGPA**: Cumulative Grade Point Average
- **SQLite**: Lightweight relational database
- **Flask**: Python web framework
- **Postman**: API testing tool

---

**Last Updated**: 2024-01-20
**Version**: 1.0.0
**Maintainer**: Your Name
