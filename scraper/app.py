from scraper.config import setup_config, Config
from scraper.session import setup_session_emex, Session


class Application():
    def __init__(self) -> None:
        self.config: Config = None
        self.session: Session = None


def setup_app():
    app = Application()
    setup_config(app, config_path='config.yml')
    setup_session_emex(app)
    return app
