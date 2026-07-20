from flask import Flask, request, jsonify
from models import db, Student
from config import config
import os

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from routes import student_bp
    app.register_blueprint(student_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': str(error)
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Method not allowed',
            'error': str(error)
        }), 405
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': str(error)
        }), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(error)
        }), 500
    
    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            'success': False,
            'message': 'Conflict',
            'error': str(error)
        }), 409
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'message': 'API is running',
            'status': 'healthy'
        }), 200
    
    return app
app = create_app(os.getenv('FLASK_ENV', 'production'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
