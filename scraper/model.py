from dataclasses import dataclass


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


@dataclass
class Session:
    request: str
    headers: str
    cookies: str

    @property
    def json(self):
        return {
            'request': self.request.body.decode('utf-8'),
            'headers': self.headers,
            'cookies': self.cookies,
        }