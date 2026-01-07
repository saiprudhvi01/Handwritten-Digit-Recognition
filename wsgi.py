import os
from app import app
from config import ProductionConfig

# Production WSGI application
application = app

if __name__ == "__main__":
    # Set production configuration
    app.config.from_object(ProductionConfig)
    
    # Create necessary directories
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/predictions', exist_ok=True)
    
    # Run with Gunicorn (recommended for production)
    # Command: gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:application
    print("Application ready for production deployment")
    print("Run with: gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:application")
