from flask import Blueprint, request, jsonify
from src.models import db
from src.models.student import Student
from src.models.class_group import ClassGroup
# from src.models.file_record import
# from src.models.user import

dashboard_bp = Blueprint('dashboard', __name__)

# --- הראוט הקיים שלך להצגת הדשבורד (דוגמה) ---
@dashboard_bp.route('/dashboard')
def show_dashboard():
    return "כאן יוצג מסך הדשבורד הראשי"


# Add new Class from route
@dashboard_bp.route('/api/classes/add', methods=['POST'])
def add_class_api():
    """
    API Endpoint to create a new class in the system and assign them to a class.
    Expects a POST request with the following JSON payload (Fetch):
    {
        "class_code": "A1", # String (Unique, Required)
        "class_name: "כיתת אגוז" # String (Unique)
    }

    Responses (JSON):
    - 201 (Created): Success - Student was successfully saved to the database.
    - 400 (Bad Request): Error - No data received or missing required fields.
    - 500 (Internal Server Error): Error - Database insertion failed or duplicate identity_num (Triggers Rollback).
    """
    data = request.get_json()

    if not data or not data.get('class_name'):
        return jsonify({"status": "error", "message": "חובה להזין שם כיתה"}), 400

    try:
        #Creating a new class (the parameters come from the fetch)
        new_class = ClassGroup(
            class_code=data.get('class_code', 'N/A'),
            class_name=data.get('class_name')
        )

        # Save command into PostgreSQL
        db.session.add(new_class)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"הכיתה {new_class.class_name} נוצרה עם ID: {new_class.id}"
        }), 201
    # In case of an error (e.g. duplicate class_code) - cancel the operation and return an error.
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Add new Student from route
@dashboard_bp.route('/api/students/add', methods=['POST'])
def add_student_api():
    """
    API Endpoint to create a new student in the system and assign them to a class.
    Expects a POST request with the following JSON payload (Fetch):
    {
        "identity_num": "123456789",  # String (Unique, Required)
        "full_name": "John Doe",       # String (Required)
        "personal_phone": "0501234567",# String (Optional)
        "class_id": 1                  # Integer (Foreign Key, Required)
    }

    Responses (JSON):
    - 201 (Created): Success - Student was successfully saved to the database.
    - 400 (Bad Request): Error - No data received or missing required fields.
    - 500 (Internal Server Error): Error - Database insertion failed or duplicate identity_num (Triggers Rollback).
    """
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "לא התקבלו נתונים"}), 400

    try:
        #Creating a new student object from the Class (the parameters come from the fetch)
        new_student = Student(
            identity_num=data.get('identity_num'),
            full_name=data.get('full_name'),
            # first_name=data.get('first_name'),
            # last_name=data.get('last_name'),
            #first_name_Hebrew=data.get('first_name_Hebrew'),
            #last_name_Hebrew=data.get('last_name_Hebrew'),
            #diagnosis=data.get('diagnosis')
            # father_name=data.get('father_name'),
            # mother_name=data.get('mother_name'),
            personal_phone=data.get('personal_phone'),
            # father_phone=data.get('father_phone'),
            # mother_phone=data.get('mother_phone'),
            # additional_phone=data.get('additional_phone'),
            # email=data.get('email'),
            # health_fund=data.get('health_fund'),
            # social_worker_name=data.get('social_worker_name'),
            # social_worker_phone=data.get('social_worker_phone'),
            class_id=int(data.get('class_id'))  # הפיכה למספר שלם (ID של הכיתה)
        )

        #Save command into PostgreSQL
        db.session.add(new_student)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"התלמיד {new_student.full_name} נוצר ונשמר בהצלחה!"
        }), 201

    except Exception as e:
        #In case of an error (e.g. duplicate ID) - cancel the operation and return an error.
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"שגיאה בשמירת התלמיד: {str(e)}"
        }), 500
