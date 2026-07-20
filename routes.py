from flask import Blueprint, request, jsonify
from models import db, Student
from sqlalchemy.exc import IntegrityError
from datetime import datetime

student_bp = Blueprint('students', __name__, url_prefix='/api/students')

# CREATE - Add a new student
@student_bp.route('', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        # Check required fields
        required_fields = ['name', 'department', 'cgpa', 'email']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate individual fields
        name = data.get('name', '').strip()
        department = data.get('department', '').strip()
        cgpa = data.get('cgpa')
        email = data.get('email', '').strip()
        
        # Name validation
        if not Student.validate_name(name):
            return jsonify({
                'success': False,
                'message': 'Name must be between 1 and 100 characters'
            }), 400
        
        # Department validation
        if not Student.validate_department(department):
            return jsonify({
                'success': False,
                'message': 'Department must be between 1 and 50 characters'
            }), 400
        
        # CGPA validation
        if not Student.validate_cgpa(cgpa):
            return jsonify({
                'success': False,
                'message': 'CGPA must be a number between 0.0 and 4.0'
            }), 400
        
        # Email validation
        if not email or not Student.validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Check if email already exists
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            return jsonify({
                'success': False,
                'message': f'Student with email {email} already exists'
            }), 409
        
        # Create new student
        student = Student(
            name=name,
            department=department,
            cgpa=float(cgpa),
            email=email
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'data': student.to_dict()
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 409
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error creating student',
            'error': str(e)
        }), 500

# READ - Get all students with pagination and filtering
@student_bp.route('', methods=['GET'])
def get_all_students():
    """Get all students with optional filtering and pagination"""
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validation
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        # Filtering
        query = Student.query
        
        # Filter by department
        department = request.args.get('department')
        if department:
            query = query.filter_by(department=department)
        
        # Filter by CGPA range
        min_cgpa = request.args.get('min_cgpa', type=float)
        max_cgpa = request.args.get('max_cgpa', type=float)
        if min_cgpa is not None:
            query = query.filter(Student.cgpa >= min_cgpa)
        if max_cgpa is not None:
            query = query.filter(Student.cgpa <= max_cgpa)
        
        # Search by name or email
        search = request.args.get('search')
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                (Student.name.ilike(search_term)) | (Student.email.ilike(search_term))
            )
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_by in ['id', 'name', 'department', 'cgpa', 'email', 'created_at', 'updated_at']:
            sort_column = getattr(Student, sort_by)
            if sort_order.lower() == 'asc':
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'message': 'Students retrieved successfully',
            'data': [student.to_dict() for student in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'total_pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error retrieving students',
            'error': str(e)
        }), 500

# READ - Get a single student by ID
@student_bp.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a single student by ID"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'message': f'Student with ID {student_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Student retrieved successfully',
            'data': student.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error retrieving student',
            'error': str(e)
        }), 500

# UPDATE - Update a student
@student_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student by ID"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'message': f'Student with ID {student_id} not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        # Update name if provided
        if 'name' in data:
            name = data['name'].strip()
            if not Student.validate_name(name):
                return jsonify({
                    'success': False,
                    'message': 'Name must be between 1 and 100 characters'
                }), 400
            student.name = name
        
        # Update department if provided
        if 'department' in data:
            department = data['department'].strip()
            if not Student.validate_department(department):
                return jsonify({
                    'success': False,
                    'message': 'Department must be between 1 and 50 characters'
                }), 400
            student.department = department
        
        # Update CGPA if provided
        if 'cgpa' in data:
            if not Student.validate_cgpa(data['cgpa']):
                return jsonify({
                    'success': False,
                    'message': 'CGPA must be a number between 0.0 and 4.0'
                }), 400
            student.cgpa = float(data['cgpa'])
        
        # Update email if provided
        if 'email' in data:
            email = data['email'].strip()
            if not Student.validate_email(email):
                return jsonify({
                    'success': False,
                    'message': 'Invalid email format'
                }), 400
            
            # Check if new email is already in use by another student
            existing_student = Student.query.filter_by(email=email).first()
            if existing_student and existing_student.id != student_id:
                return jsonify({
                    'success': False,
                    'message': f'Student with email {email} already exists'
                }), 409
            
            student.email = email
        
        student.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully',
            'data': student.to_dict()
        }), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 409
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error updating student',
            'error': str(e)
        }), 500

# DELETE - Delete a student
@student_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student by ID"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'message': f'Student with ID {student_id} not found'
            }), 404
        
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student deleted successfully',
            'data': student.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error deleting student',
            'error': str(e)
        }), 500

# STATISTICS - Get student statistics
@student_bp.route('/stats/summary', methods=['GET'])
def get_statistics():
    """Get statistics about students"""
    try:
        total_students = Student.query.count()
        
        if total_students == 0:
            return jsonify({
                'success': True,
                'message': 'Statistics retrieved successfully',
                'data': {
                    'total_students': 0,
                    'average_cgpa': 0,
                    'highest_cgpa': None,
                    'lowest_cgpa': None,
                    'departments': {}
                }
            }), 200
        
        from sqlalchemy import func
        
        # Calculate statistics
        avg_cgpa = db.session.query(func.avg(Student.cgpa)).scalar()
        max_cgpa = db.session.query(func.max(Student.cgpa)).scalar()
        min_cgpa = db.session.query(func.min(Student.cgpa)).scalar()
        
        # Get department distribution
        departments = db.session.query(
            Student.department,
            func.count(Student.id).label('count')
        ).group_by(Student.department).all()
        
        dept_dict = {dept: count for dept, count in departments}
        
        return jsonify({
            'success': True,
            'message': 'Statistics retrieved successfully',
            'data': {
                'total_students': total_students,
                'average_cgpa': round(avg_cgpa, 2) if avg_cgpa else 0,
                'highest_cgpa': round(max_cgpa, 2) if max_cgpa else None,
                'lowest_cgpa': round(min_cgpa, 2) if min_cgpa else None,
                'departments': dept_dict
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error retrieving statistics',
            'error': str(e)
        }), 500