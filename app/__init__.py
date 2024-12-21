from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create upload directory if it doesn't exist
    os.makedirs(os.path.join('app', 'static', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join('app', 'static', 'generated'), exist_ok=True)
    
    return app