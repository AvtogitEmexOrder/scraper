import random
import time
import typing

if typing.TYPE_CHECKING:
    from web import Application

from selenium.webdriver.common.by import By
from seleniumwire import webdriver


class Session:

    def __init__(self, app) -> None:
        self.app: Application = app

    def timeout(self):
        time.sleep(random.choice((range(2, 4))))

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


def setup_session_emex(app):
    session = Session(app)
    app.session = session.run()
