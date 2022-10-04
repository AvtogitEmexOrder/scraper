from dataclasses import dataclass

import yaml


@dataclass
class Proxy:
    login: str
    password: str
    host: str
    port: str


@dataclass
class SettingSelenium:
    useragent: str
    chromedriver: str


@dataclass
class Emex:
    host: str
    login: str
    password: str
    api_order: str


@dataclass
class Config:
    emex: Emex
    selenium: SettingSelenium
    proxy: Proxy


def setup_config(app, config_path: str):
    with open(config_path, 'r') as f:
        raw_config = yaml.safe_load(f)

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
