"""
WSGI Entry Point for Production
Used by Gunicorn to serve the Flask application
"""

from web.app import create_app

# Create app instance (Gunicorn needs just the Flask app, not socketio)
app, socketio = create_app()

# Export app for Gunicorn
application = app
