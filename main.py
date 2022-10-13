from flask import Flask
from scraper.view import session
from scraper.errors import AppError

app = Flask(__name__)

def handle_app_errors(error: AppError):
    return {'error': error.reason}, 500

app.register_blueprint(session, url_prefix='/api/v1/session/')

app.register_error_handler(AppError, handle_app_errors)


if __name__ == "__main__":
    app.run(host='0.0.0.0')