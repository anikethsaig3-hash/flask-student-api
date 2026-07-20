# How to Run Flask Student API - Step-by-Step Guide

## Prerequisites Check

Before starting, ensure you have:
- Python 3.7+ installed
- pip (Python package manager)
- Git installed
- A terminal/command prompt

**Check Python version:**
```bash
python --version
# or
python3 --version
```

Should show: `Python 3.7.0` or higher

---

## Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/anikethsaig3-hash/flask-student-api.git
cd flask-student-api
```

**What this does:**
- Downloads the project from GitHub
- Changes into the project directory

**Expected output:**
```
Cloning into 'flask-student-api'...
remote: Counting objects: 100% (20/20), done.
remote: Compressing objects: 100% (15/15), done.
remote: Receiving objects: 100% (20/20), 15.32 KiB | 15.32 MiB/s, done.
Resolving deltas: 100% (5/5), done.
```

---

## Step 2: Create Virtual Environment

Creating a virtual environment isolates project dependencies.

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**What this does:**
- Creates a folder called `venv` with isolated Python environment
- Activates the virtual environment

**How to know it's activated:**
Your terminal prompt should show `(venv)` at the beginning:
```
(venv) C:\Users\YourName\flask-student-api>
```

---

## Step 3: Install Dependencies

With virtual environment activated, run:

```bash
pip install -r requirements.txt
```

**What this installs:**
```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
SQLAlchemy==2.0.19
python-dotenv==1.0.0
```

**Expected output:**
```
Collecting Flask==2.3.2
  Downloading Flask-2.3.2-py3-none-any.whl (101 kB)
Installing collected packages: click, itsdangerous, Werkzeug, Jinja2, Flask, ...
Successfully installed Flask-2.3.2 Flask-SQLAlchemy-3.0.5 SQLAlchemy-2.0.19 python-dotenv-1.0.0
```

---

## Step 4: Setup Environment Variables (Optional)

The `.env.example` file already has defaults configured.

To use custom settings:

```bash
cp .env.example .env
```

Then edit `.env` if needed (usually not necessary for development):
```
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=True
```

---

## Step 5: Seed the Database (Optional but Recommended)

This populates the database with 12 sample students for testing:

```bash
python seed.py
```

**Expected output:**
```
✓ Database seeded successfully with 12 students

Seeded students:
  - John Doe (Computer Science) - CGPA: 3.8 - john.doe@university.edu
  - Jane Smith (Electronics) - CGPA: 3.9 - jane.smith@university.edu
  - Michael Johnson (Computer Science) - CGPA: 3.6 - michael.johnson@university.edu
  ... (and 9 more)
```

**What this creates:**
- `students.db` - SQLite database file
- 12 sample student records

---

## Step 6: Run the Application

Start the Flask API server:

```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
 * Debugger is active!
 * Debugger PIN: 123-456-789
```

The API is now running at: **http://localhost:5000**

---

## Step 7: Verify API is Working

Open a **new terminal window** (keep the first one running) and test the API:

### Quick Health Check:
```bash
curl http://localhost:5000/health
```

**Expected response:**
```json
{
  "success": true,
  "message": "API is running",
  "status": "healthy"
}
```

### Get All Students:
```bash
curl http://localhost:5000/api/students
```

**Expected response:**
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
    ... (11 more students)
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 12,
    "total_pages": 2
  }
}
```

### Create a New Student:
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Test",
    "department": "Mechanical",
    "cgpa": 3.7,
    "email": "alice@test.edu"
  }'
```

**Expected response:**
```json
{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 13,
    "name": "Alice Test",
    "department": "Mechanical",
    "cgpa": 3.7,
    "email": "alice@test.edu",
    "created_at": "2024-01-20T14:30:45",
    "updated_at": "2024-01-20T14:30:45"
  }
}
```

---

## Step 8: Run Unit Tests (Optional)

In the **second terminal** (not the one running the API), run:

```bash
python -m unittest test_api.py -v
```

**Expected output:**
```
test_cgpa_boundary_values (test_api.StudentAPITestCase) ... ok
test_create_student_duplicate_email (test_api.StudentAPITestCase) ... ok
test_create_student_empty_name (test_api.StudentAPITestCase) ... ok
test_create_student_invalid_cgpa (test_api.StudentAPITestCase) ... ok
test_create_student_invalid_email (test_api.StudentAPITestCase) ... ok
test_create_student_missing_fields (test_api.StudentAPITestCase) ... ok
test_create_student_success (test_api.StudentAPITestCase) ... ok
test_delete_student_not_found (test_api.StudentAPITestCase) ... ok
test_delete_student_success (test_api.StudentAPITestCase) ... ok
... (40+ tests total)
----------------------------------------------------------------------
Ran 40 tests in 0.234s

OK
```

---

## Complete Running Flow (Summary)

```bash
# 1. Clone repository
git clone https://github.com/anikethsaig3-hash/flask-student-api.git
cd flask-student-api

# 2. Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed database with sample data
python seed.py

# 5. Run the API
python app.py

# 6. In another terminal, test the API
curl http://localhost:5000/health

# 7. Run unit tests (optional)
python -m unittest test_api.py -v
```

---

## Common Issues & Solutions

### Issue: "Python not found"
**Solution:**
```bash
# Try python3 instead
python3 --version
python3 -m venv venv
```

### Issue: "venv\Scripts\activate not found" (Windows)
**Solution:** Use forward slashes:
```bash
source venv/Scripts/activate
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Ensure virtual environment is activated (should see `(venv)` in prompt):
```bash
# Check if activated
which python  # macOS/Linux - should show path with 'venv'
where python  # Windows - should show path with 'venv'

# If not activated:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Issue: "Port 5000 already in use"
**Solution:** Use a different port:
```bash
# Edit app.py last line or run with:
python app.py --port 5001
```

Or kill the process using port 5000:
```bash
# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: "Database file not found"
**Solution:** Seed the database:
```bash
python seed.py
```

### Issue: Tests fail
**Solution:** Ensure database is clean:
```bash
# Remove old database
rm students.db

# Reseed
python seed.py

# Run tests again
python -m unittest test_api.py -v
```

---

## Testing with Postman (GUI Method)

Instead of curl commands, you can use Postman for a visual interface:

### 1. Download Postman
Go to https://www.postman.com/downloads/

### 2. Import Collection
1. Open Postman
2. Click "Import"
3. Select `Flask_Student_API.postman_collection.json` from the project folder
4. All 30+ pre-configured requests will be imported

### 3. Set Base URL
1. In Postman, go to "Manage Environments"
2. Create new environment or edit existing
3. Set variable `base_url` = `http://localhost:5000`

### 4. Start Testing
- Click on any request in the collection
- Click "Send"
- View response in the bottom panel

---

## Testing with Web Browser (GUI Method)

Open `index.html` in your browser:

1. Go to project folder
2. Right-click `index.html`
3. Select "Open with" → Your browser
4. View all documentation and endpoints
5. Click on links to GitHub docs

---

## Directory Structure After Running

```
flask-student-api/
├── app.py
├── models.py
├── routes.py
├── config.py
├── seed.py
├── test_api.py
├── requirements.txt
├── .env.example
├── .env (created)
├── .gitignore
├── students.db (created after seed.py)
├── venv/ (created - virtual environment)
├── API_DOCUMENTATION.md
├── README.md
├── index.html
└── Flask_Student_API.postman_collection.json
```

---

## Stopping the API

To stop the API server:

**In the terminal running the API, press:**
```
CTRL + C
```

**Expected output:**
```
^CTraceback (most recent call last):
  File "app.py", line X, in <module>
    app.run(debug=True, host='0.0.0.0', port=5000)
KeyboardInterrupt
```

---

## Deactivating Virtual Environment

When done working, deactivate the virtual environment:

```bash
deactivate
```

The `(venv)` prefix should disappear from your prompt.

---

## Troubleshooting Checklist

- [ ] Python 3.7+ installed
- [ ] Virtual environment created and activated (`(venv)` in prompt)
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] Database seeded (`python seed.py`)
- [ ] API running (`python app.py` - shows port 5000)
- [ ] Health check passes (`curl http://localhost:5000/health`)
- [ ] Tests pass (`python -m unittest test_api.py -v`)

---

## Quick Reference Commands

```bash
# Activate virtual environment
venv\Scripts\activate              # Windows
source venv/bin/activate           # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed.py

# Run API
python app.py

# Run tests
python -m unittest test_api.py -v

# Test health
curl http://localhost:5000/health

# Get all students
curl http://localhost:5000/api/students

# Create student
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","department":"CS","cgpa":3.5,"email":"test@test.edu"}'

# Deactivate virtual environment
deactivate
```

---

## Next Steps

After running the API:

1. **Explore Endpoints** - Try different API calls
2. **Read Documentation** - Check `API_DOCUMENTATION.md`
3. **Use Postman** - Import `Flask_Student_API.postman_collection.json`
4. **Run Tests** - Execute `python -m unittest test_api.py -v`
5. **Review Code** - Understand the implementation
6. **Deploy** - Use Gunicorn or Docker for production

---

## Additional Resources

- 📖 Full API Docs: `API_DOCUMENTATION.md`
- 📚 README: `README.md`
- 🧪 Tests: `test_api.py`
- 📡 Postman Collection: `Flask_Student_API.postman_collection.json`
- 🌐 Interactive Docs: `index.html`
- 🔗 GitHub: https://github.com/anikethsaig3-hash/flask-student-api

---

**You're all set! Start with `python app.py` and enjoy the API! 🚀**
