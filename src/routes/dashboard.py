from flask import Blueprint, request, jsonify
from src.models import db
import src.controllers.student_controller as student_ctrl
import src.controllers.class_group_controller as class_ctrl
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
    return class_ctrl.add_class_logic()

# Add new Student from route
@dashboard_bp.route('/api/students/add', methods=['POST'])
def add_student_api():
    return student_ctrl.add_student_logic()


# Get all Students for the dashboard table
@dashboard_bp.route('/api/students', methods=['GET'])
def get_all_students_api():
    return student_ctrl.get_all_students_logic()

# Get students on request for the dashboard table
@dashboard_bp.route('/api/students/search', methods=['GET'])
def search_students_api():
    return student_ctrl.get_students_by_search_logic()