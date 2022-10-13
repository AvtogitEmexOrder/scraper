import yaml

from scraper.errors import NotFoundFileConfigError, NotFoundKeyConfigError
from scraper.model import Config, Emex, Proxy, SettingSelenium


def setup_config(app, config_path: str):
    try:
        with open(config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
    except FileNotFoundError:
        raise NotFoundFileConfigError('NotFound file config')

    try:
        app.config = Config(
            emex=Emex(
                host=raw_config['emex']['host'],
                login=raw_config['emex']['login'],
                password=raw_config['emex']['password'],
                api_order=raw_config['emex']['api_order'],
            ),
            selenium=SettingSelenium(
                useragent=raw_config['selenium']['useragent'],
                chromedriver=raw_config['selenium']['chromedriver'],
            ),
            proxy=Proxy(
                login=raw_config['proxy']['login'],
                password=raw_config['proxy']['password'],
                host=raw_config['proxy']['host'],
                port=raw_config['proxy']['port'],
            ),
        )
    except KeyError:
        raise NotFoundKeyConfigError('NotFound Key in file config')
