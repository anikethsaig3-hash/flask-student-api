from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

db = SQLAlchemy()

class Student(db.Model):
    """Student model with validation"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'
    
    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'cgpa': self.cgpa,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_cgpa(cgpa):
        """Validate CGPA is between 0.0 and 4.0"""
        try:
            cgpa_float = float(cgpa)
            return 0.0 <= cgpa_float <= 4.0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_name(name):
        """Validate name is not empty and has reasonable length"""
        return isinstance(name, str) and 1 <= len(name.strip()) <= 100
    
    @staticmethod
    def validate_department(department):
        """Validate department is not empty and has reasonable length"""
        return isinstance(department, str) and 1 <= len(department.strip()) <= 50