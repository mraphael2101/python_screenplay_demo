import pytest

from testlib.interactions import *
from testlib.models import BtHomePage


@pytest.mark.regression
def test_login_scenario_using_tasks(browser):
    actor = Actor("Mark")
    actor.can_use(browser=browser)
    """
    - An instance of an actor is created via the test fixture
      in conftest.py and passed into the test via dependency
      injection
    """
    print("The name of the actor is -> " + actor.name)
    """
    - has() -> returns a boolean based on the lookup
      of a key in a dictionary 
    """
    print("Actor has the browser ability -> " + str(actor.has("browser")))
    # Tasks
    actor.attempts_to(Load(BtHomePage.URL))
    actor.attempts_to(HandleCookiePolicyOnHomePage())
    actor.attempts_to(NavigateFromHomePageTo("My BT"))
    actor.attempts_to(VerifyResultPageTitleContains("Login Page"))
    actor.attempts_to(EnterAndSubmitCredentialsToLogin("invalid_username", "invalid_password"))


@pytest.mark.regression
def test_label_validation_with_questions(browser) -> None:
    actor = Actor("Mark")
    actor.can_use(browser=browser)  # Without this you cannot manipulate Selenium
    # Tasks
    actor.attempts_to(Load(BtHomePage.URL))
    actor.attempts_to(HandleCookiePolicyOnHomePage())
    actor.attempts_to(NavigateFromHomePageTo("Broadband"))  # Task
    # Question
    caption = actor.asks_for(LabelAttribute(By.XPATH, "//input[@id='sc-postcode']"))
    assert "Postcode" in caption
    # Question -> Same concept as line 34 but uses a different wording
    # actor.calls()


