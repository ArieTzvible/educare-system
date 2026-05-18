import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://user:{os.getenv('DB_PASSWORD')}@localhost/db"
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    BACKUP_PATH = os.getenv('BACKUP_PATH')


print('config.py - print 1')
print('1. Config.SECRET_KEY =',Config.SECRET_KEY)
print('2. Config.UPLOAD_FOLDER = ',Config.UPLOAD_FOLDER)
print('3. Config.BACKUP_PATH =',Config.BACKUP_PATH)
print('-------------')