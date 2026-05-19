from flask import request, jsonify
from src.models import db
from src.models.student import Student

def add_student_logic():
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
        # Creating a new student object from the Class (the parameters come from the fetch)
        new_student = Student(
            identity_num=data.get('identity_num'),
            full_name=data.get('full_name'),
            # first_name=data.get('first_name'),
            # last_name=data.get('last_name'),
            # first_name_Hebrew=data.get('first_name_Hebrew'),
            # last_name_Hebrew=data.get('last_name_Hebrew'),
            # diagnosis=data.get('diagnosis')
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

        # Save command into PostgreSQL
        db.session.add(new_student)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"התלמיד {new_student.full_name} נוצר ונשמר בהצלחה!"
        }), 201

    except Exception as e:
        # In case of an error (e.g. duplicate ID) - cancel the operation and return an error.
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"שגיאה בשמירת התלמיד: {str(e)}"
        }), 500


def get_all_students_logic():
        """
        API Endpoint to fetch all students with their class details for the dashboard table.

        Responses (JSON):
        - 200 (OK): Returns a list of all students.
        - 500 (Internal Server Error): Error fetching data.
        """
        try:
            #Retrieving all students from the database
            students = Student.query.all()

            students_list = []
            for student in students:
                students_list.append({
                    "id": student.id,
                    "identity_num": student.identity_num,
                    "full_name": student.full_name,
                    "personal_phone": student.personal_phone,
                    "class_name": student.class_group.class_name if student.class_group else "ללא כיתה"
                })

            return jsonify({
                "status": "success",
                "data": students_list
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"שגיאה בשליפת הנתונים: {str(e)}"
            }), 500


def get_students_by_search_logic():
    """Fetches students with dynamic filtering and dynamically includes the filtered fields in the response."""
    try:
        # Retrieving the parameters
        query_params = request.args.to_dict()
        query = Student.query
        valid_filters = []

        # Building a dynamic query
        for key, value in query_params.items():
            if hasattr(Student, key):
                model_attr = getattr(Student, key)
                query = query.filter(model_attr == value)
                valid_filters.append(key)

        # Running the query against the database
        students = query.order_by(Student.full_name.asc()).all()

        # JSON construction
        students_list = []
        for student in students:
            # הנתונים הבסיסיים שתמיד יופיעו
            student_data = {
                "id": student.id,
                "identity_num": student.identity_num,
                "full_name": student.full_name,
                "personal_phone": student.personal_phone,
                "status": student.status,
                "class_name": student.class_group.class_name if student.class_group else "ללא כיתה"
            }

            # Adding the fields from the request
            for filter_field in valid_filters:
                if filter_field != 'class_id':
                    student_data[filter_field] = getattr(student, filter_field, None)

            students_list.append(student_data)

        return jsonify({
            "status": "success",
            "type": "dynamic_generic_search",
            "filters_applied": query_params,
            "count": len(students_list),
            "data": students_list
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500