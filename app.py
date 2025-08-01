from flask import Flask
from markdown import markdown
from api.register import register_blueprints
from core.data_layer.sql import setup_sqlite_from_config
from core.data_layer.images import create_image_table

def create_app():
    app = Flask(__name__)
    
    # Set secret key for session management (required for flash messages)
    app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

    # Register blueprints from the api.v1 package
    register_blueprints(app, 'api.v1')

    with app.app_context():
        setup_sqlite_from_config()
        create_image_table()
    
    # Add a filter for markdown
    @app.template_filter('markdown')
    def markdown_filter(s):
        return markdown(s)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)