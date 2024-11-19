# tests/conftest.py
import allure
import pytest
from selene.support.shared import browser

from api.base_api import BaseApi
from config import USER_EMAIL, USER_PASSWORD


def pytest_runtest_setup(item):
    """
    Hook to dynamically add fixtures based on test markers.
    """
    if "ui" in item.keywords:
        print(f"Setting up UI environment for test: {item.name}")
        item.fixturenames.append("setup_browser")
    elif "api" in item.keywords:
        print(f"Setting up API environment for test: {item.name}")
        item.fixturenames.append("authorized_api")
    elif "integration" in item.keywords:
        print(f"Setting up Integration environment for test: {item.name}")
        item.fixturenames.append("setup_browser")
        item.fixturenames.append("authorized_api")

@pytest.fixture(scope="function")
def setup_browser():
    #browser.config.base_url = "https://"
    browser.config.window_width = 1200
    browser.config.window_height = 800
    yield
    if browser.driver:
        try:
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Screenshot creating error: {e}")
        finally:
            browser.quit()



@pytest.fixture(scope="session")
def auth_token():
    response = BaseApi().request('POST', 'auth/login', json={
        'identifier': USER_EMAIL,
        'password': USER_PASSWORD
    })
    if response.status_code != 201:
        pytest.fail(f"Authentication failed: {response.text}")
    return response.json().get('data', {}).get('accessToken')


@pytest.fixture
def authorized_api(auth_token):
    api = BaseApi()
    api.session.headers['Authorization'] = f'Bearer {auth_token}'
    return api

@pytest.fixture
def integration_fixture(setup_browser, authorized_api):
    """Combines UI and API setup for integration tests."""
    return {
        "browser": browser,
        "api": authorized_api,
    }