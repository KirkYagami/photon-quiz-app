from flask import Flask
from flask_mail import Mail
from config import Config

# Initialize extensions
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Flask-Mail with app
    mail.init_app(app)
    
    # Register blueprints
    from routes.main import main
    from routes.quiz import quiz
    from routes.admin import admin
    from routes.support import support
    
    app.register_blueprint(main)
    app.register_blueprint(quiz)
    app.register_blueprint(admin)
    app.register_blueprint(support)
    
    return app