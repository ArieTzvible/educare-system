from flask import Blueprint, request, jsonify
from src.models import db
from src.models.student import Student

dashboard_bp = Blueprint('dashboard', __name__)


# --- הראוט הקיים שלך להצגת הדשבורד (דוגמה) ---
@dashboard_bp.route('/dashboard')
def show_dashboard():
    return "כאן יוצג מסך הדשבורד הראשי"


# --- 🚀 הראוט החדש ליצירת תלמיד חדש מה-Fetch ---
@dashboard_bp.route('/api/students/add', methods=['POST'])
def add_student_api():
    # 1. תפיסת ה-JSON שהגיע מהדפדפן
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "לא התקבלו נתונים"}), 400

    try:
        # 2. יצירת אובייקט תלמיד חדש מתוך ה-Class (הפרמטרים מגיעים מה-fetch)
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

        # 3. פקודת שמירה לתוך ה-PostgreSQL
        db.session.add(new_student)
        db.session.commit()

        # 4. החזרת תשובת הצלחה לפרונטאנד
        return jsonify({
            "status": "success",
            "message": f"התלמיד {new_student.full_name} נוצר ונשמר בהצלחה!"
        }), 201

    except Exception as e:
        # במקרה של שגיאה (למשל תעודת זהות כפולה) - מבטלים את הפעולה ומחזירים שגיאה
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"שגיאה בשמירת התלמיד: {str(e)}"
        }), 500
