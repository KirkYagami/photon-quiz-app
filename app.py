from flask import Flask
from config import Config
from routes.main import main
from routes.admin import admin
from routes.quiz import quiz

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(quiz)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("="*50)
    app.run(debug=True, host='0.0.0.0',port=5000)