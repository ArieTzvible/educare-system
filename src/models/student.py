from src.models import db


class Student(db.Model):
    __tablename__ = 'students'

    # --- שדות חובה וזיהוי ליבה ---
    id = db.Column(db.Integer, primary_key=True)
    identity_num = db.Column(db.String(9), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    # -----------------------------
    # first_name = db.Column(db.String(100), nullable=False)
    # last_name = db.Column(db.String(100), nullable=False)
    # first_name_Hebrew = db.Column(db.String(100), nullable=True)
    # last_name_Hebrew = db.Column(db.String(100), nullable=True)
    # diagnosis = db.Column(db.String(100), nullable=True)
    #
    # father_name = db.Column(db.String(100), nullable=True)
    # mother_name = db.Column(db.String(100), nullable=True)
    #
    # # --- פרטי התקשרות ---
    personal_phone = db.Column(db.String(20), nullable=True)
    # father_phone = db.Column(db.String(20), nullable=True)
    # mother_phone = db.Column(db.String(20), nullable=True)
    # additional_phone = db.Column(db.String(20), nullable=True)  # טלפון נוסף לחירום
    # email = db.Column(db.String(120), nullable=True)
    #
    # # --- פרטי רפואה ורווחה  ---
    # health_fund = db.Column(db.String(50), nullable=True)  # קופת חולים (כללית, מכבי וכו')
    # social_worker_name = db.Column(db.String(100), nullable=True)  # עו"ס עירייה
    # social_worker_phone = db.Column(db.String(20), nullable=True)  # טלפון עו"ס
    #
    # address = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='active')  # פעיל / לא פעיל

    # --- מפתחות זרים וקשרים ---
    # המפתח הזר שמחבר את התלמיד לכיתה שלו
    class_id = db.Column(db.Integer, db.ForeignKey('class_groups.id'), nullable=False)

    # קשר לקבצים האישיים של התלמיד (מוגדר בטבלת הקבצים)
    files = db.relationship('FileRecord', backref='student', lazy=True)

    def __repr__(self):
        return f"<Student {self.full_name}>"