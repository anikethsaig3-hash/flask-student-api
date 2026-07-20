import unittest
import json
from app import create_app
from models import db, Student

class StudentAPITestCase(unittest.TestCase):
    """Test cases for Flask Student API"""
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Seed test data
            self.seed_test_data()
    
    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def seed_test_data(self):
        """Add sample students for testing"""
        students = [
            Student(name='John Doe', department='Computer Science', cgpa=3.8, email='john@test.edu'),
            Student(name='Jane Smith', department='Electronics', cgpa=3.9, email='jane@test.edu'),
            Student(name='Mike Johnson', department='Mechanical', cgpa=3.5, email='mike@test.edu'),
        ]
        for student in students:
            db.session.add(student)
        db.session.commit()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'healthy')
    
    # CREATE Tests
    def test_create_student_success(self):
        """Test successful student creation"""
        payload = {
            'name': 'Alice Brown',
            'department': 'Civil',
            'cgpa': 3.7,
            'email': 'alice@test.edu'
        }
        response = self.client.post('/api/students', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Alice Brown')
        self.assertEqual(data['data']['email'], 'alice@test.edu')
    
    def test_create_student_missing_fields(self):
        """Test student creation with missing required fields"""
        payload = {'name': 'Test Student'}
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Missing required fields', data['message'])
    
    def test_create_student_invalid_email(self):
        """Test student creation with invalid email format"""
        payload = {
            'name': 'Test Student',
            'department': 'Computer Science',
            'cgpa': 3.5,
            'email': 'invalid-email'
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Invalid email format', data['message'])
    
    def test_create_student_invalid_cgpa(self):
        """Test student creation with CGPA out of range"""
        payload = {
            'name': 'Test Student',
            'department': 'Computer Science',
            'cgpa': 4.5,
            'email': 'test@test.edu'
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('CGPA must be a number between 0.0 and 4.0', data['message'])
    
    def test_create_student_duplicate_email(self):
        """Test student creation with duplicate email"""
        payload = {
            'name': 'Duplicate Test',
            'department': 'Computer Science',
            'cgpa': 3.5,
            'email': 'john@test.edu'  # Already exists
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('already exists', data['message'])
    
    def test_create_student_empty_name(self):
        """Test student creation with empty name"""
        payload = {
            'name': '',
            'department': 'Computer Science',
            'cgpa': 3.5,
            'email': 'test@test.edu'
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # READ Tests
    def test_get_all_students(self):
        """Test retrieving all students"""
        response = self.client.get('/api/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 3)
        self.assertIn('pagination', data)
        self.assertEqual(data['pagination']['total'], 3)
    
    def test_get_all_students_pagination(self):
        """Test student retrieval with pagination"""
        response = self.client.get('/api/students?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['per_page'], 2)
        self.assertEqual(data['pagination']['total_pages'], 2)
    
    def test_get_all_students_filter_by_department(self):
        """Test filtering students by department"""
        response = self.client.get('/api/students?department=Computer%20Science')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['department'], 'Computer Science')
    
    def test_get_all_students_filter_by_cgpa_range(self):
        """Test filtering students by CGPA range"""
        response = self.client.get('/api/students?min_cgpa=3.7&max_cgpa=4.0')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 2)  # John and Jane
        for student in data['data']:
            self.assertGreaterEqual(student['cgpa'], 3.7)
            self.assertLessEqual(student['cgpa'], 4.0)
    
    def test_get_all_students_search_by_name(self):
        """Test searching students by name"""
        response = self.client.get('/api/students?search=john')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], 'John Doe')
    
    def test_get_all_students_search_by_email(self):
        """Test searching students by email"""
        response = self.client.get('/api/students?search=jane')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['email'], 'jane@test.edu')
    
    def test_get_all_students_sort_by_cgpa_desc(self):
        """Test sorting students by CGPA in descending order"""
        response = self.client.get('/api/students?sort_by=cgpa&sort_order=desc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data'][0]['cgpa'], 3.9)
        self.assertEqual(data['data'][1]['cgpa'], 3.8)
        self.assertEqual(data['data'][2]['cgpa'], 3.5)
    
    def test_get_all_students_sort_by_name_asc(self):
        """Test sorting students by name in ascending order"""
        response = self.client.get('/api/students?sort_by=name&sort_order=asc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data'][0]['name'], 'Jane Smith')
        self.assertEqual(data['data'][1]['name'], 'John Doe')
        self.assertEqual(data['data'][2]['name'], 'Mike Johnson')
    
    def test_get_all_students_combined_filters(self):
        """Test combined filtering, searching, and sorting"""
        response = self.client.get('/api/students?min_cgpa=3.5&sort_by=cgpa&sort_order=desc&page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(data['data'][0]['cgpa'], 3.9)
    
    def test_get_single_student(self):
        """Test retrieving a single student by ID"""
        response = self.client.get('/api/students/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], 1)
        self.assertEqual(data['data']['name'], 'John Doe')
    
    def test_get_student_not_found(self):
        """Test retrieving non-existent student"""
        response = self.client.get('/api/students/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('not found', data['message'])
    
    # UPDATE Tests
    def test_update_student_success(self):
        """Test successful student update"""
        payload = {'cgpa': 3.95, 'department': 'Electronics'}
        response = self.client.put('/api/students/1',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['cgpa'], 3.95)
        self.assertEqual(data['data']['department'], 'Electronics')
        self.assertEqual(data['data']['name'], 'John Doe')  # Unchanged
    
    def test_update_student_partial(self):
        """Test partial student update"""
        payload = {'cgpa': 3.85}
        response = self.client.put('/api/students/1',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data']['cgpa'], 3.85)
        self.assertEqual(data['data']['name'], 'John Doe')
    
    def test_update_student_invalid_cgpa(self):
        """Test updating student with invalid CGPA"""
        payload = {'cgpa': 5.0}
        response = self.client.put('/api/students/1',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_invalid_email(self):
        """Test updating student with invalid email"""
        payload = {'email': 'invalid-email'}
        response = self.client.put('/api/students/1',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_duplicate_email(self):
        """Test updating student with duplicate email"""
        payload = {'email': 'jane@test.edu'}  # Already taken
        response = self.client.put('/api/students/1',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_not_found(self):
        """Test updating non-existent student"""
        payload = {'cgpa': 3.9}
        response = self.client.put('/api/students/999',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # DELETE Tests
    def test_delete_student_success(self):
        """Test successful student deletion"""
        response = self.client.delete('/api/students/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('deleted', data['message'])
        
        # Verify deletion
        response = self.client.get('/api/students/1')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_student_not_found(self):
        """Test deleting non-existent student"""
        response = self.client.delete('/api/students/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # STATISTICS Tests
    def test_get_statistics(self):
        """Test getting student statistics"""
        response = self.client.get('/api/students/stats/summary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        stats = data['data']
        
        self.assertEqual(stats['total_students'], 3)
        self.assertEqual(stats['average_cgpa'], 3.73)  # (3.8 + 3.9 + 3.5) / 3
        self.assertEqual(stats['highest_cgpa'], 3.9)
        self.assertEqual(stats['lowest_cgpa'], 3.5)
        self.assertIn('Computer Science', stats['departments'])
        self.assertEqual(stats['departments']['Computer Science'], 1)
    
    def test_get_statistics_after_deletion(self):
        """Test statistics after deleting a student"""
        self.client.delete('/api/students/1')
        response = self.client.get('/api/students/stats/summary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        stats = data['data']
        
        self.assertEqual(stats['total_students'], 2)
        self.assertEqual(stats['highest_cgpa'], 3.9)
        self.assertEqual(stats['lowest_cgpa'], 3.5)
    
    def test_get_statistics_empty_database(self):
        """Test statistics with empty database"""
        # Delete all students
        self.client.delete('/api/students/1')
        self.client.delete('/api/students/2')
        self.client.delete('/api/students/3')
        
        response = self.client.get('/api/students/stats/summary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        stats = data['data']
        
        self.assertEqual(stats['total_students'], 0)
        self.assertEqual(stats['average_cgpa'], 0)
        self.assertIsNone(stats['highest_cgpa'])
        self.assertIsNone(stats['lowest_cgpa'])
    
    # VALIDATION Tests
    def test_validate_name_length(self):
        """Test name validation for length"""
        payload = {
            'name': 'A' * 101,  # Too long
            'department': 'Computer Science',
            'cgpa': 3.5,
            'email': 'test@test.edu'
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_validate_department_length(self):
        """Test department validation for length"""
        payload = {
            'name': 'Test',
            'department': 'A' * 51,  # Too long
            'cgpa': 3.5,
            'email': 'test@test.edu'
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_cgpa_boundary_values(self):
        """Test CGPA with boundary values"""
        # Test with CGPA = 0.0 (valid)
        payload = {
            'name': 'Test 1',
            'department': 'CS',
            'cgpa': 0.0,
            'email': 'test1@test.edu'
        }
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # Test with CGPA = 4.0 (valid)
        payload['email'] = 'test2@test.edu'
        payload['cgpa'] = 4.0
        response = self.client.post('/api/students',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    # EDGE CASES
    def test_get_all_students_invalid_pagination(self):
        """Test invalid pagination parameters"""
        response = self.client.get('/api/students?page=-1&per_page=0')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Should use default values
        self.assertEqual(data['pagination']['page'], 1)
    
    def test_get_all_students_max_per_page(self):
        """Test maximum per_page limit"""
        response = self.client.get('/api/students?per_page=150')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Should cap at 100
        self.assertEqual(data['pagination']['per_page'], 10)  # Uses default if too high
    
    def test_update_student_empty_body(self):
        """Test updating student with empty request body"""
        response = self.client.put('/api/students/1',
                                  data=json.dumps({}),
                                  content_type='application/json')
        # Should succeed but not change anything (or fail with empty body error)
        self.assertIn(response.status_code, [200, 400])


if __name__ == '__main__':
    unittest.main()
