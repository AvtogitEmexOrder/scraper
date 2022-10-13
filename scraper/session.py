import random
import time
import typing
from dataclasses import dataclass

from scraper.errors import (
    InvalidSelectorSeleniumError, 
    NoSuchElementError, 
    NotFoundRequestError,
)

if typing.TYPE_CHECKING:
    from app import Application

from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
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
            'request': self.request.body.decode('utf-8'),
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
        #TODO: Когда не верный логин и пароль, что делать?!
        try:
            self.enter_website(driver)
            self.login(driver)
            self.enter_orders(driver)
        except InvalidSelectorException:
            raise InvalidSelectorSeleniumError('Invalid selector selenium')
        except NoSuchElementException:
            raise NoSuchElementError('Selenium not found such element, maybe the page didn\'t load')

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
        raise NotFoundRequestError('Not Found Request in driver')

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return {c['name']: c['value'] for c in cookies}

    def get_headers(self):
        response = self.request.headers._headers
        headers = {header[0]: header[1] for header in response}
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
