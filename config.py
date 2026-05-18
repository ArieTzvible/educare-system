import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://user:{os.getenv('DB_PASSWORD')}@localhost/db"
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    BACKUP_PATH = os.getenv('BACKUP_PATH')