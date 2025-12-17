import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'quiz_app.db')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    DEFAULT_QUIZ_TIMER = 30  # minutes
    PASSING_SCORE = 70  # percentage
    
    # Session config for production
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 7200  # 2 hours