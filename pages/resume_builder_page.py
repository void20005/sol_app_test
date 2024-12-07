from selene import be

from config import BASE_URL
from locators.resume_builder_locators import ResumeBuilderLocators
from pages.base_page import BasePage
from selene.support.shared.jquery_style import ss, s
import allure


class ResumeBuilderPage(BasePage):
    @allure.step("Get all rows from the resume table")
    def get_table_rows(self):
        """Returns all rows from the resume table."""
        return ss(ResumeBuilderLocators.ROWS)

    @allure.step("Click on the 'Create New Resume' button")
    def click_create_new_resume(self):
        """Clicks on the 'Create New Resume' button."""
        self.click(ResumeBuilderLocators.CREATE_NEW_RESUME_BUTTON)

    @allure.step("Get resume name from row {row_index}")
    def get_resume_name(self, row_index: int):
        """Gets the text of the resume name from the specified row."""
        row = self.get_table_rows()[row_index]
        return row.element(ResumeBuilderLocators.ROW_NAME).text

    @allure.step("Click action button in row {row_index}")
    def click_action_button(self, row_index: int):
        """Clicks on the action button in the specified row."""
        row = self.get_table_rows()[row_index]
        row.element(ResumeBuilderLocators.ROW_ACTION_BUTTON).click()

    @allure.step("Open resume for editing from row {row_index}")
    def open_resume_for_editing(self, row_index: int):
        """Clicks on a row to open the resume editing page."""
        self.get_table_rows()[row_index].click()

    @allure.step("Navigate to Resume Builder page")
    def open_resume_builder_page(self):
        """Navigates to the Resume Builder page."""
        self.open(BASE_URL + "resumes")
        s(ResumeBuilderLocators.TABLE).with_(timeout=2).should(be.visible)
        return self
