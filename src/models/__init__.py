from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from src.models.class_group import ClassGroup
from src.models.student import Student
# from src.models.teacher import Teacher
# from src.models.file_record import FileRecord