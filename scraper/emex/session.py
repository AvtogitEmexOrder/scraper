import orjson
import random
import time
import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from app import Application

from selenium.webdriver.common.by import By
from seleniumwire import webdriver


@dataclass
class Session:
    request: str
    headers: str
    cookies: str

    @property
    def json(self):
        return {
            'request': str(self.request.body),
            'headers': self.headers,
            'cookies': self.cookies,
        }


class Surfing:

    def __init__(self, app) -> None:
        self.app: Application = app

    def timeout(self):
        time.sleep(random.choice((range(3, 4))))

    def setting(self):
        options = webdriver.ChromeOptions()
        options.add_argument(self.app.config.selenium.useragent)
        options.add_argument("window-size=1200x600")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        return options

    def proxy(self) -> dict[str, dict[str, str]]:
        proxy_options = {
            'proxy': {
                'https': f'http://{self.app.config.proxy.login}:{self.app.config.proxy.password}@{self.app.config.proxy.host}:{self.app.config.proxy.port}'
            }
        }
        return proxy_options

    def enter_website(self, driver):
        driver.get(self.app.config.emex.host)
        self.timeout()

    def login(self, driver):
        driver.find_element(By.CLASS_NAME, 'lk2gmii').click()
        self.timeout()
        login_input = driver.find_element(By.ID, 'signInLoginInput')
        login_input.clear()
        login_input.send_keys(self.app.config.emex.login)
        self.timeout()
        password_input = driver.find_element(By.ID, 'signInPasswordInput')
        password_input.clear()
        password_input.send_keys(self.app.config.emex.password)
        self.timeout()
        driver.find_element(By.CLASS_NAME, 'l1iy1epa').click()
        self.timeout()

    def enter_orders(self, driver):
        driver.find_element(By.CLASS_NAME, 'l-inmotion').click()
        self.timeout()

    def run(self):
        driver = webdriver.Chrome(
            executable_path=self.app.config.selenium.chromedriver,
            options=self.setting(),
            seleniumwire_options=self.proxy()
        )
        self.enter_website(driver)
        self.login(driver)
        self.enter_orders(driver)

        return driver


class Parsing:

    def __init__(self, app, driver) -> None:
        self.app: Application = app
        self.driver = driver
        self.request = self.get_request()
        self.headers = self.get_headers()
        self.cookies = self.get_cookies()

    def get_request(self):
        for requst in self.driver.requests:
            if requst.url == self.app.config.emex.api_order:
                return requst

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        cookie = {c['name']: c['value'] for c in cookies}
        return cookie

    def get_headers(self):
        headers = {}
        response = self.request
        payload = response.headers._headers
        for header in payload:
            headers[header[0]] = header[1]
        del headers['Content-Length']
        return headers


def setup_session_emex(app):
    surfing = Surfing(app)
    driver = surfing.run()
    pars = Parsing(app, driver)
    driver.quit()

    app.session = Session(
        request=pars.request,
        headers=pars.headers,
        cookies=pars.cookies,
    )
