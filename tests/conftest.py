import logging
import pytest
from selene.support.shared import browser
from api.base_api import BaseApi
from config import USER_EMAIL, USER_PASSWORD, STATUS_OK, BASE_URL
from data.generator_data import GeneratorData
from pages.login_page import LoginPage
from locators.login_locators import LoginLocators



logger = logging.getLogger(__name__)

@pytest.fixture()
def setup_browser():
    browser.config.base_url=BASE_URL
    browser.config.window_width=1200
    browser.config.window_height=800
    yield
    browser.quit()

@pytest.fixture()
def login(setup_browser):
    """Authorization before each test function."""
    page = LoginPage()
    page.open(BASE_URL + "/login")
    page.login(USER_EMAIL, USER_PASSWORD)
    page.should_see_element(LoginLocators.LOGOUT_BUTTON)
    yield
    ##

@pytest.fixture(scope="session")
def auth_token():
    response = BaseApi().request('POST', 'auth/login', json={
        'identifier': USER_EMAIL,
        'password': USER_PASSWORD
    })
    token = response.json().get('data', {}).get('accessToken')
    if not token:
        pytest.fail("Authentication token not found in response.")
    return token


@pytest.fixture(scope="session")

def authorized_api(auth_token):
    api = BaseApi()
    api.session.headers['Authorization'] = f'Bearer {auth_token}'
    return api


@pytest.fixture
def auth_api_data(request, authorized_api):
    data = GeneratorData()
    def cleanup():
        for resume_id in data.resume_valid_ids:
            try:
                response = authorized_api.request("DELETE", f"resume-ats/{resume_id}")
                if response.status_code != STATUS_OK:
                    logger.warning(f"Failed to delete resume {resume_id} with status code {response.status_code}")
            except Exception as e:
                logger.error(f"Error while deleting resume {resume_id}: {e}")
        for resume_id in data.base_resume_valid_ids:
            try:
                response = authorized_api.request("DELETE", f"base-resumes/{resume_id}")
                if response.status_code != STATUS_OK:
                    logger.warning(f"Failed to delete base resume {resume_id} with status code {response.status_code}")
            except Exception as e:
                logger.error(f"Error while deleting base resume {resume_id}: {e}")
    request.addfinalizer(cleanup)
    yield authorized_api, data


@pytest.fixture
def integration_fixture(setup_browser, authorized_api):
    """Combines UI and API setup for integration tests."""
    return {
        "browser": browser,
        "api": authorized_api
    }