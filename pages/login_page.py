# pages/login_page.py
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    @allure.step("Log in with email: {email}")
    def login(self, email: str, password: str):
        """Performs login using the provided email and password."""
        self.type_text("[name='identifier']", email)
        self.type_text("[name='password']", password)
        self.click("button[type='submit']")
        return self

    @allure.step("Click 'Forgot Password'")
    def forgot_password(self):
        """Clicks on the 'Forgot Password?' link."""
        self.click("a").with_text("Forgot Password?")
        return self

    @allure.step("Click 'Sign Up'")
    def sign_up(self):
        """Clicks on the 'Sign Up' link."""
        self.click("a").with_text("Sign Up")
        return self

    @allure.step("Sign in with Google")
    def sign_in_with_google(self):
        """Clicks on the 'Sign in with Google' button."""
        self.click("[aria-label='Sign in with Google']")
        return self
