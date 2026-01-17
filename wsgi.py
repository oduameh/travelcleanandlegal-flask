"""
WSGI entry point for production deployment.
Usage: gunicorn wsgi:app -b 0.0.0.0:8000
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
