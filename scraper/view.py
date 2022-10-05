from flask import Blueprint, json
from scraper.app import Application, run_app


session = Blueprint('session', __name__)


@session.get('/emex')
def get_session():
    app: Application = run_app()
    return json.dumps(app.session.json)