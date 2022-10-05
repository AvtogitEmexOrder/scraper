from flask import Flask
from scraper.view import session

app = Flask(__name__)

app.register_blueprint(session, url_prefix='/api/v1/session/')


if __name__ == "__main__":
    app.run(host='0.0.0.0')