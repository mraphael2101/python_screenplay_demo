import json
import requests
import pytest
from requests import Session

from screenplay.pattern import Actor
from selenium.webdriver import Chrome, ChromeOptions, Firefox
from selenium.webdriver.remote.webdriver import WebDriver

"""
This module contains shared fixtures to handle setup and teardown
"""


@pytest.fixture
def config(scope='session') -> dict:
    with open('../config.json') as config_file:
        config = json.load(config_file)

    if 'browser' in config.keys():
        assert config['browser'] in ['Firefox', 'Chrome', 'Headless Chrome']
    if 'http_library' in config.keys():
        assert config['http_library'] in ['requests', 'pyhttptest']
    return config


# Object is passed in via DI returned from config method above
@pytest.fixture
def browser(config: dict) -> WebDriver:
    if config['browser'] == 'Firefox':
        browser = Firefox()
    elif config['browser'] == 'Chrome':
        browser = Chrome()
    elif config['browser'] == 'Headless Chrome':
        opts = ChromeOptions()
        opts.add_argument('headless')
        browser = Chrome(options=opts)
    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    browser.implicitly_wait(10)

    yield browser  # Return the WebDriver instance for the setup

    browser.quit()


# Object is passed in via DI returned from config method above
@pytest.fixture
def http_library(config: dict) -> Session:
    """
    A Session object allows one to persist certain parameters across requests.
    It also persists cookies across all requests made from the Session instance.
    So, if several requests are being made to the same host, the underlying TCP
    connection will be reused which can result in a significant performance increase
    """
    if config['http_library'].lower() == 'requests':
        session = requests.Session()
        return session
    elif config['http_library'].lower() == 'pyhttptest':
        raise Exception("pyhttptest library not supported yet")


