from src.models import db


class ClassGroup(db.Model):
    __tablename__ = 'class_groups'

    id = db.Column(db.Integer, primary_key=True)
    class_code = db.Column(db.String(50), unique=True, nullable=False)  # למשל: A1, B2
    class_name = db.Column(db.String(100), nullable=False)  # למשל: כיתה א' 1

    # קשרים (Relationships) - משתמשים במחרוזות כדי למנוע קריסה של פייתון

    # קשר לתלמידים בכיתה (אחד לרבים)
    students = db.relationship('Student', backref='class_group', lazy=True)

    # קשר לקבצים של הכיתה (אחד לרבים)
    files = db.relationship('FileRecord', backref='class_group', lazy=True)

    # תשתית עתידית: קשר למערכת שעות (למשל טבלת Schedule)
    # schedule = db.relationship('Schedule', backref='class_group', lazy=True)

    # תשתית עתידית: קשר למורים (קשר של רבים לרבים - כי מורה מלמד בכמה כיתות, ובכיתה יש כמה מורים)
    # teachers = db.relationship('Teacher', seconday='class_teachers', backref='classes')

    def __repr__(self):
        return f"<ClassGroup {self.class_name}>"