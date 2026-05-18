import os
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


def save_uploaded_file(file, entity_type, entity_id, report_type, user_name):
    """
    מנהל את השמירה הכפולה: שרת + גיבוי
    entity_id: ת.ז של תלמיד או קוד כיתה (למשל '123456789' או 'class_a1')
    entity_type: 'students' או 'classes'
    """

    # יצירת חותמת זמן ושם קובץ מאובטח
    time = datetime.now().strftime("%H-%M")
    date = datetime.now().strftime("%Y-%m-%d")
    original_ext = os.path.splitext(file.filename)[1].lower()

    # בניית שם הקובץ: סוג-דוח_מזהה_תאריך_הועלה-ע-י.סיומת
    # אנחנו משתמשים ב-secure_filename כדי לנקות תווים בעייתיים
    filename = f"{report_type}_{entity_id}_{time}_by_{user_name}{original_ext}"
    safe_filename = secure_filename(filename)

    # שליפת נתיבים מה-Config
    base_server = current_app.config['UPLOAD_FOLDER']
    base_backup = current_app.config['BACKUP_PATH']

    # בניית תתי-התיקיות (למשל: students/123456789/tala/)
    relative_path = os.path.join(entity_type, str(entity_id), report_type, date)

    server_dir = os.path.join(base_server, relative_path)
    backup_dir = os.path.join(base_backup, relative_path)

    # יצירת התיקיות פיזית אם לא קיימות
    os.makedirs(server_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    server_path = os.path.join(server_dir, safe_filename)
    backup_path = os.path.join(backup_dir, safe_filename)

    # שמירה לשרת העבודה
    file.save(server_path)

    # העתקה לגיבוי (Immutable - העותק בגיבוי לא יימחק לעולם ע"י משתמש רגיל)
    shutil.copy2(server_path, backup_path)

    return {
        "storage_path": server_path,
        "backup_path": backup_path,
        "final_name": safe_filename
    }