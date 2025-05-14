from flask_cors import CORS
import os

def configure_cors(app):
    frontend = os.getenv('FRONTEND_URL')
    backend = os.getenv('BACKEND_URL')
    origins = [frontend, backend]
    return CORS(
        app,
        resources={r"/api/*": {"origins": origins}},
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        expose_headers='Authorization',
        methods="OPTIONS,GET,HEAD,POST"
    )