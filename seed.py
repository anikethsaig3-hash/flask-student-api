"""
Database seeding script to populate initial student data
"""

from app import create_app
from models import db, Student
from datetime import datetime, timedelta
import random

def seed_database():
    """Seed the database with sample student data"""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        Student.query.delete()
        db.session.commit()
        
        # Sample data
        departments = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Electrical']
        
        students_data = [
            {
                'name': 'John Doe',
                'department': 'Computer Science',
                'cgpa': 3.8,
                'email': 'john.doe@university.edu'
            },
            {
                'name': 'Jane Smith',
                'department': 'Electronics',
                'cgpa': 3.9,
                'email': 'jane.smith@university.edu'
            },
            {
                'name': 'Michael Johnson',
                'department': 'Computer Science',
                'cgpa': 3.6,
                'email': 'michael.johnson@university.edu'
            },
            {
                'name': 'Emily Williams',
                'department': 'Mechanical',
                'cgpa': 3.7,
                'email': 'emily.williams@university.edu'
            },
            {
                'name': 'David Brown',
                'department': 'Civil',
                'cgpa': 3.5,
                'email': 'david.brown@university.edu'
            },
            {
                'name': 'Sarah Jones',
                'department': 'Electrical',
                'cgpa': 3.85,
                'email': 'sarah.jones@university.edu'
            },
            {
                'name': 'Robert Garcia',
                'department': 'Computer Science',
                'cgpa': 3.4,
                'email': 'robert.garcia@university.edu'
            },
            {
                'name': 'Lisa Martinez',
                'department': 'Electronics',
                'cgpa': 3.75,
                'email': 'lisa.martinez@university.edu'
            },
            {
                'name': 'James Wilson',
                'department': 'Mechanical',
                'cgpa': 3.3,
                'email': 'james.wilson@university.edu'
            },
            {
                'name': 'Maria Anderson',
                'department': 'Civil',
                'cgpa': 3.9,
                'email': 'maria.anderson@university.edu'
            },
            {
                'name': 'Christopher Taylor',
                'department': 'Electrical',
                'cgpa': 3.65,
                'email': 'christopher.taylor@university.edu'
            },
            {
                'name': 'Jennifer Thomas',
                'department': 'Computer Science',
                'cgpa': 3.88,
                'email': 'jennifer.thomas@university.edu'
            }
        ]
        
        # Create student objects and add to session
        for data in students_data:
            student = Student(
                name=data['name'],
                department=data['department'],
                cgpa=data['cgpa'],
                email=data['email']
            )
            db.session.add(student)
        
        # Commit all at once
        db.session.commit()
        
        print(f"✓ Database seeded successfully with {len(students_data)} students")
        print("\nSeeded students:")
        for student in Student.query.all():
            print(f"  - {student.name} ({student.department}) - CGPA: {student.cgpa} - {student.email}")

if __name__ == '__main__':
    seed_database()