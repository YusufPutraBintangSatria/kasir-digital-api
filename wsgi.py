"""
WSGI entry point untuk production deployment
Used by Gunicorn pada Railway
"""

from app import app

if __name__ == "__main__":
    app.run()
