import allure
import pytest

from pages.login_page import LoginPage
from config import BASE_URL, USER_EMAIL, USER_PASSWORD
from selene.support.shared.jquery_style import s
from selene.support.conditions import be, have


@allure.tag('web')
@allure.severity(allure.severity_level.BLOCKER)
@allure.feature('Authentication')
@allure.story('Successful login')
@pytest.mark.ui
def test_successful_login():
    login_page = LoginPage()
    # Step 1: Open the login page
    login_page.open(BASE_URL + "/login")
    # Step 2: Perform login
    login_page.login(USER_EMAIL, USER_PASSWORD)
    # Step 3: Verify successful login
    s('button[aria-label="Sign out"]').should(be.visible)

@allure.tag("web")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Authentication")
@allure.story("Sign in with Google")
@pytest.mark.ui
@pytest.mark.skipif(True, reason="function not developed yet")
def test_google_authorization():
    login_page = LoginPage()

    # Step 1: Open the login page
    login_page.open(BASE_URL + "/login")

    # Step 2: Click on 'Sign in with Google'
    login_page.sign_in_with_google()

    # Step 3: Verify redirection to Google login page
    s("title").should(have.exact_text("Sign in – Google accounts"))