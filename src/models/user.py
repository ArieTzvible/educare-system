# src/models/user.py
from datetime import datetime
from src.models import db
from werkzeug.security import generate_password_hash, check_password_hash

# 🏫 טבלת הקשר שמחזיקה את קודי הכיתות הספציפיים של העובדים
user_classes = db.Table('user_classes',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
                                  primary_key=True),
                        db.Column('class_id', db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'),
                                  primary_key=True)
                        )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    identity_num = db.Column(db.String(9), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # פרטים אישיים
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    role_title = db.Column(db.String(50), nullable=True)  # תואר העובד (למשל: "מחנכת", "פסיכולוג")

    # --------- Permissions ------------------------
    # Class access type: 'NONE', 'ALL', 'SPECIFIC'.
    class_access_type = db.Column(db.String(20), default='NONE', nullable=False)
    # File access level: 'none', 'limited_read', 'full_read', 'edit'
    file_access_level = db.Column(db.String(20), default='none', nullable=False)
    # create/update an employee (team management)
    can_manage_staff = db.Column(db.Boolean, default=False, nullable=False)
    # Access to employee timesheets
    can_view_staff_schedule = db.Column(db.Boolean, default=False, nullable=False)
    # Changing class assignments for students and teachers
    can_change_class_assignments = db.Column(db.Boolean, default=False, nullable=False)

    # --------------------------------------------------------

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Linking authorized classes
    classes = db.relationship('ClassGroup', secondary=user_classes, backref=db.backref('staff_members', lazy='dynamic'))
    # New employee (password change required)
    needs_password_change = db.Column(db.Boolean, default=True, nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.identity_num} - Access: {self.class_access_type}>'