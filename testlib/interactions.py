from requests import Response, Session
from screenplay.pattern import Actor, Task, Question
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from testlib.pages import BtHomePage, BTLoginPage

"""
This module contains web UI interactions for BT.com
"""

# Questions


class LabelAttribute(Question[str]):
    def __init__(self, by: By, query: str) -> None:
        self.by = by
        self.query = query

    def request_as(self, actor: Actor) -> str:
        browser: WebDriver = actor.using('browser')
        input = browser.find_element(self.by, self.query)
        value = input.get_attribute('aria-label')
        return value


class TextListFor(Question[list[str]]):
    def __init__(self, by: By, query: str) -> None:
        self.by = by
        self.query = query

    def request_as(self, actor: Actor) -> list[str]:
        browser: WebDriver = actor.using('browser')
        links = browser.find_elements(self.by, self.query)
        titles = [link.text for link in links]
        return titles


class Title(Question[str]):
    def request_as(self, actor: Actor) -> str:
        browser: WebDriver = actor.using('browser')
        return browser.title


class CallReqResApi(Question[str]):
    def __init__(self, url: str) -> None:
        self.url = url

    def request_as(self, actor: Actor) -> Response:
        http_lib: Session = actor.using('http_library')
        response = http_lib.get(self.url)
        return response


# Tasks

class Load(Task):
    def __init__(self, url: str) -> None:
        self.url = url

    def perform_as(self, actor: Actor) -> None:
        browser: WebDriver = actor.using('browser')
        browser.get(self.url)


class HandleCookiePolicyOnHomePage(Task):
    def perform_as(self, actor: Actor) -> None:
        browser: WebDriver = actor.using('browser')
        browser.implicitly_wait(5)
        # browser.switch_to.frame(browser.find_element(By.XPATH, "//iframe[@title='TrustArc Cookie Consent Manager']"))
        browser.add_cookie({"name": "notice_gdpr_prefs", "value": "0|1|2|3:"})
        browser.refresh()


class NavigateFromHomePageTo(Task):
    def __init__(self, option: str) -> None:
        self.option = option.lower()

    def perform_as(self, actor: Actor) -> None:
        b: WebDriver = actor.using('browser')
        if self.option == "my bt":
            for num in range(0, 2):
                b.find_element(*BtHomePage.MY_BT_LINK).click()
            b.add_cookie({"name": "cmapi_cookie_privacy", "value": "permit_1|2|3|4",
                          "name": "notice_gdpr_prefs", "value": "3:"})
            b.refresh()
        if self.option == "broadband":
            for num in range(0, 2):
                b.find_element(*BtHomePage.BROADBAND_LINK).click()


class VerifyResultPageTitleContains(Task):
    def __init__(self, phrase: str) -> None:
        self.phrase = phrase

    def perform_as(self, actor: Actor) -> None:
        title = actor.asks_for(Title())
        assert self.phrase in title


class EnterAndSubmitCredentialsToLogin(Task):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def perform_as(self, actor: Actor) -> None:
        browser: WebDriver = actor.using('browser')
        username_input = browser.find_element(*BTLoginPage.USERNAME_INPUT)
        username_input.send_keys(self.username + Keys.RETURN)
        password_input = browser.find_element(*BTLoginPage.PASSWORD_INPUT)
        password_input.send_keys(self.password + Keys.RETURN)
        if not browser.find_element(*BTLoginPage.ERROR_NOTIFICATION_CON).is_displayed():
            browser.find_element(*BTLoginPage.LOGIN_BTN).click()
