import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('FLASK_DATABASE_URI', 'sqlite:///default.db')

# Initialize Database
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(1), nullable=False)

def initialize_database():
    """Create database tables only if they don't exist."""
    with app.app_context():
        engine = db.engine  # Get SQLAlchemy engine
        inspector = inspect(engine)  
        if not inspector.get_table_names():  # Check if tables exist
            db.create_all()
            logging.info("✅ Database tables created.")

# JSON Validation Helper Function
def validate_json(required_fields):
    if not request.is_json:
        logging.warning("Request must be JSON")
        return None, (jsonify({"error": "Request must be JSON"}), 415)
    
    data = request.get_json(silent=True)
    if not data:
        logging.warning("Invalid or empty JSON payload")
        return None, (jsonify({"error": "Invalid or empty JSON payload"}), 400)
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logging.warning(f"Missing fields: {', '.join(missing_fields)}")
        return None, (jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400)
    
    return data, None


@app.route('/api/v1/students', methods=['POST'])
def add_student():
    required_fields = ["first_name", "last_name", "age", "sex"]
    data, error = validate_json(required_fields)
    if error:
        return error
    
    try:
        new_student = Student(
            first_name=data['first_name'], 
            last_name=data['last_name'], 
            age=data['age'], 
            sex=data['sex']
        )
        db.session.add(new_student)
        db.session.commit()
        logging.info("Student added successfully")
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        logging.error(f"Error adding student: {e}")
        return jsonify({'error': 'An error occurred while adding the student'}), 500

@app.route('/api/v1/students', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()
        return jsonify([
            {'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name, 'age': s.age, 'sex': s.sex} 
            for s in students
        ])
    except Exception as e:
        logging.error(f"Error fetching students: {e}")
        return jsonify({'error': 'An error occurred while fetching students'}), 500

@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        student = Student.query.get_or_404(id)
        return jsonify({
            'id': student.id, 
            'first_name': student.first_name, 
            'last_name': student.last_name, 
            'age': student.age, 
            'sex': student.sex
        })
    except Exception as e:
        logging.error(f"Error fetching student {id}: {e}")
        return jsonify({'error': 'An error occurred while fetching the student'}), 500

@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    required_fields = ["first_name", "last_name", "age", "sex"]
    data, error = validate_json(required_fields)
    if error:
        return error
    
    try:
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.age = data.get('age', student.age)
        student.sex = data.get('sex', student.sex)

        db.session.commit()
        logging.info(f"Student {id} updated successfully")
        return jsonify({'message': 'Student updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating student {id}: {e}")
        return jsonify({'error': 'An error occurred while updating the student'}), 500

@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        logging.info(f"Student {id} deleted successfully")
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting student {id}: {e}")
        return jsonify({'error': 'An error occurred while deleting the student'}), 500

if __name__ == '__main__':
    initialize_database() 

    logging.info("Starting Flask application...")
    app.run(host="0.0.0.0")