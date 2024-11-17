# pages/base_page.py
from selene.support.shared import browser
from selene.support.shared.jquery_style import s
from selene.support.conditions import be
from selene import have
import allure


class BasePage:
    @allure.step("Open URL: {url}")
    def open(self, url: str):
        """Opens the specified page."""
        browser.open(url)
        return self

    @allure.step("Click on element: {locator}")
    def click(self, locator: str):
        """Clicks on the element after ensuring it is visible."""
        s(locator).should(be.visible).click()
        return self

    @allure.step("Type text '{text}' into element: {locator}")
    def type_text(self, locator: str, text: str):
        """Clears the input field and types the specified text."""
        s(locator).should(be.visible).clear().type(text)
        return self

    @allure.step("Verify page title is: {title}")
    def should_have_title(self, title: str):
        """Verifies that the page title matches the expected value."""
        browser.should(have.title(title))
        return self

    @allure.step("Verify element is visible: {locator}")
    def should_see_element(self, locator: str):
        """Ensures that the specified element is visible on the page."""
        s(locator).should(be.visible)
        return self
