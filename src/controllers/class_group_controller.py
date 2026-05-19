from flask import request, jsonify
from src.models import db
from src.models.class_group import ClassGroup

def add_class_logic():
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
