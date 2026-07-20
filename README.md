# Flask Student API

A comprehensive REST API for managing student records built with Flask and SQLite.

## Features

✨ **Complete CRUD Operations**
- Create, Read, Update, Delete student records
- Batch operations support

🔍 **Advanced Search & Filtering**
- Filter by department, CGPA range
- Search by name or email
- Pagination support
- Flexible sorting options

✅ **Validation & Error Handling**
- Email format validation
- CGPA range validation (0.0 - 4.0)
- Input sanitization
- Comprehensive error messages
- HTTP status codes

📊 **Statistics**
- Calculate average CGPA
- Get highest/lowest CGPA
- Department distribution

💾 **Database**
- SQLite for easy deployment
- SQLAlchemy ORM
- Automatic timestamps

## Requirements

- Python 3.7+
- Flask 2.3.2
- Flask-SQLAlchemy 3.0.5
- SQLAlchemy 2.0.19

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-student-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

## Quick Start

### 1. Seed the database with sample data
```bash
python seed.py
```

### 2. Run the application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Check API health
```bash
curl http://localhost:5000/health
```

## API Endpoints

### Students

#### Create a new student
```http
POST /api/students
Content-Type: application/json

{
  "name": "John Doe",
  "department": "Computer Science",
  "cgpa": 3.8,
  "email": "john.doe@university.edu"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Student created successfully",
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

#### Get all students
```http
GET /api/students
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10, max: 100)
- `department` - Filter by department
- `min_cgpa` - Minimum CGPA
- `max_cgpa` - Maximum CGPA
- `search` - Search by name or email
- `sort_by` - Sort field (id, name, department, cgpa, email, created_at, updated_at)
- `sort_order` - Sort order (asc, desc - default: desc)

**Example:**
```bash
curl "http://localhost:5000/api/students?page=1&per_page=5&department=Computer%20Science&sort_by=cgpa&sort_order=desc"
```

#### Get a single student
```http
GET /api/students/{id}
```

**Example:**
```bash
curl http://localhost:5000/api/students/1
```

#### Update a student
```http
PUT /api/students/{id}
Content-Type: application/json

{
  "cgpa": 3.9,
  "department": "Electronics"
}
```

#### Delete a student
```http
DELETE /api/students/{id}
```

#### Get statistics
```http
GET /api/students/stats/summary
```

**Response (200):**
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

## Validation Rules

### Name
- Required
- String type
- Length: 1-100 characters

### Department
- Required
- String type
- Length: 1-50 characters

### CGPA
- Required
- Numeric value (float)
- Range: 0.0 - 4.0

### Email
- Required
- Valid email format
- Unique (no duplicates)
- Pattern: `name@domain.extension`

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Name must be between 1 and 100 characters"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Student with ID 999 not found"
}
```

### 409 Conflict
```json
{
  "success": false,
  "message": "Student with email john@university.edu already exists"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error",
  "error": "Error details"
}
```

## Project Structure

```
flask-student-api/
├── app.py                 # Flask application factory and error handlers
├── models.py              # Student model and database
├── routes.py              # API endpoints (CRUD operations)
├── config.py              # Configuration settings
├── seed.py                # Database seeding script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables example
├── .gitignore             # Git ignore rules
├── students.db            # SQLite database (auto-created)
└── README.md              # This file
```

## Testing

### Test creating a student
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

### Test filtering by CGPA
```bash
curl "http://localhost:5000/api/students?min_cgpa=3.7&max_cgpa=4.0"
```

### Test searching
```bash
curl "http://localhost:5000/api/students?search=john"
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=True
```

## Configuration

Three configuration profiles available in `config.py`:

- **Development**: Debug mode enabled, useful for development
- **Production**: Debug mode disabled, optimized for production
- **Testing**: Uses in-memory SQLite database

## Database

The API uses SQLite for data persistence. The database file (`students.db`) is created automatically in the project root when you run the application.

### Database Schema

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(100) | Not Null, Indexed |
| department | String(50) | Not Null |
| cgpa | Float | Not Null |
| email | String(120) | Not Null, Unique, Indexed |
| created_at | DateTime | Not Null, Default: Current time |
| updated_at | DateTime | Not Null, Default: Current time |

## Best Practices

1. **Always validate input** - Use provided validation methods
2. **Check for duplicates** - Email must be unique
3. **Handle errors gracefully** - All endpoints return proper HTTP status codes
4. **Use pagination** - For large datasets, use pagination parameters
5. **Keep credentials safe** - Never commit `.env` files

## Contributing

1. Create a new branch for features
2. Follow PEP 8 style guide
3. Add tests for new functionality
4. Update documentation

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue in the repository.