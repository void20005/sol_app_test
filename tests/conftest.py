# tests/conftest.py
import pytest
from selene.support.shared import browser

@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    #browser.config.base_url = "https://example.com"
    browser.config.window_width = 1200
    browser.config.window_height = 800
    yield
    browser.quit()
