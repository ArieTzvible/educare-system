# src/controllers/user_controller.py
from flask import request, jsonify
from src.models import db
from src.models.user import User
from src.models.class_group import ClassGroup


def create_user_logic():
    """Creates a new staff member with fine-grained permissions and class assignments."""
    try:
        data = request.get_json()

        identity_num = data.get('identity_num')
        if User.query.filter_by(identity_num=identity_num).first():
            return jsonify({"status": "error", "message": "עובד עם תעודת זהות זו כבר קיים במערכת"}), 400

        # Create user
        new_user = User(
            identity_num=identity_num,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            role_title=data.get('role_title'),

            # Setting permissions
            class_access_type=data.get('class_access_type', 'NONE').upper(),  # NONE, ALL, SPECIFIC
            file_access_level=data.get('file_access_level', 'none'),  # none, limited_read, full_read, edit
            can_manage_staff=data.get('can_manage_staff', False),
            can_view_staff_schedule=data.get('can_view_staff_schedule', False),
            can_change_class_assignments=data.get('can_change_class_assignments', False)
        )

        # Setting the initial password
        initial_password = data.get('password', identity_num)
        new_user.set_password(initial_password)

        #Class list association
        if new_user.class_access_type == 'SPECIFIC':
            class_ids = data.get('class_ids', [])
            if class_ids:
                assigned_classes = ClassGroup.query.filter(ClassGroup.id.in_(class_ids)).all()
                new_user.classes = assigned_classes

        # Saving in a database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "העובד נוצר בהצלחה במערכת",
            "user_id": new_user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500