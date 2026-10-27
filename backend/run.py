import os
from flask import Flask
from flask_cors import CORS
from app.config import settings
from app.extensions import db
from app.routes.health import health_bp
from app.routes.evidence import evidence_bp
from app.routes.analysis import analysis_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = settings.MAX_UPLOAD_SIZE
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS
    cors_origins = settings.CORS_ORIGINS.split(',')
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    app.register_blueprint(evidence_bp, url_prefix='/api/v1/evidence')
    app.register_blueprint(analysis_bp, url_prefix='/api/v1/analysis')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Ensure storage directories exist
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(settings.EVIDENCE_FOLDER, exist_ok=True)
    os.makedirs(settings.REPORTS_FOLDER, exist_ok=True)
    os.makedirs(settings.THUMBNAILS_FOLDER, exist_ok=True)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.FLASK_DEBUG
    )
