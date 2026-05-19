from flask import Flask
from src.config import Config
from src.models import db


def create_app():
    # 1. יצירת מופע האפליקציה של Flask
    app = Flask(__name__)

    # 2. טעינת ההגדרות מקובץ ה-config
    app.config.from_object(Config)

    # 3. אתחול מסד הנתונים עם האפליקציה
    db.init_app(app)

    # 4. רישום ה-Blueprints (נתיבי השרת) - מייבאים פה בפנים למניעת בעיות מעגליות
    from src.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app