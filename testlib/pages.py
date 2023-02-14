from selenium.webdriver.common.by import By


class BtHomePopupPage:
    COOKIES_CONSENT_BTN = (By.XPATH, "//a[contains(text(), 'Accept all cookies')]")


class BtLoginPopupPage:
    COOKIES_CONSENT_BTN = (By.XPATH, "//a[contains(text(), 'Accept all cookies')]")


class BtHomePage:
    URL = "https://www.bt.com/"
    MY_BT_LINK = (By.XPATH, "//li[@class='bt-navbar-screen-md-main']//span[contains(text(),'My BT')]")
    BROADBAND_LINK = (By.XPATH, "//li[@class='bt-navbar-screen-xs-max-main']//span[contains(text(),'Broadband')]")


class BTLoginPage:
    URL = "https://home.bt.com/login/loginform"
    ERROR_NOTIFICATION_CON = (By.XPATH, "//div[contains(@class, 'loginerror')]")
    USERNAME_INPUT = (By.XPATH, "//input[@name='USER']")
    PASSWORD_INPUT = (By.NAME, "NAFMPASSWORD")
    LOGIN_BTN = (By.XPATH, "//input[@value='Log in to My BT']")
