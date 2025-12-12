import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'quiz_app.db')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    DEFAULT_QUIZ_TIMER = 30  # minutes
    PASSING_SCORE = 70  # percentage