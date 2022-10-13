from flask import Blueprint, json
from scraper.app import Application, setup_app


session = Blueprint('session', __name__)


@session.get('/emex')
def get_session():
    app: Application = setup_app()
    return json.dumps(app.session.json)
