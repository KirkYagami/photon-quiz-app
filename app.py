from flask import Flask
from config import Config
from routes.main import main
from routes.admin import admin
from routes.quiz import quiz



from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(quiz)
    
    # Add template filters
    from utils.helpers import render_markdown
    app.jinja_env.filters['markdown'] = render_markdown

    app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
    x_prefix=1
    )

    
    return app

if __name__ == '__main__':
    app = create_app()
    print("="*50)
    print("Starting QuizFlow in development mode")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)
