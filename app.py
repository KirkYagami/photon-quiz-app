from flask import Flask
from config import Config
from routes.main import main
from routes.admin import admin
from routes.quiz import quiz
from routes.support import support

from dotenv import load_dotenv
load_dotenv()




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(quiz)
    app.register_blueprint(support)
    
    # Add template filters
    from utils.helpers import render_markdown
    app.jinja_env.filters['markdown'] = render_markdown
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("="*50)
    print("Starting QuizFlow in development mode")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)