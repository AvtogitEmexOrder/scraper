from scraper.config import setup_config, Config
from scraper.emex.session import setup_session_emex


class Application():
    def __init__(self) -> None:
        self.config: Config = None
        self.session = None


def run_app():
    app = Application()
    setup_config(app, config_path='config.yml')
    setup_session_emex(app)