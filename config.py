import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base directory
    BASE_DIR = Path(__file__).parent
    
    # Database
    DATABASE_PATH = BASE_DIR / 'quiz_app.db'
    
    # Admin credentials
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Change this!
    
    # Quiz settings
    DEFAULT_QUIZ_TIMER = 30  # minutes
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Email settings for SMTP
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', '')
    
    # Admin email to receive contact form submissions
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'er.nikhilsharma7@gmail.com')