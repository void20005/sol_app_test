import logging
import time
import warnings

import allure
import pytest
from selene import be
from selene.core import query
from selene.support.conditions import have
from selene.support.shared.jquery_style import s, ss

from config import BASE_URL, USER_EMAIL, USER_PASSWORD
from pages.resume_builder_page import ResumeBuilderPage
from locators.resume_builder_locators import ResumeBuilderLocators as RB_Loc


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

@allure.feature("Resume Builder RB_UI 1.1")
@allure.story("Check Resume Builder page is open")
@pytest.mark.ui
@pytest.mark.smoke
def test_open_resume_builder_page(login):
    page = ResumeBuilderPage()
    page.open(BASE_URL + 'resumes')
    #page.open_resume_builder_page()
    assert page.should_see_element(RB_Loc.CREATE_NEW_RESUME_BUTTON), \
        "Create Resume Button is not found"
    assert page.should_see_element(RB_Loc.TAILOR_RESUME_BUTTON), \
        "Tailor Resume Button is not found"
    assert page.should_see_element(RB_Loc.TABLES_HEAD), "Resumes Table is not found"
    text = s(RB_Loc.PAGE_NAME_TEXT).get(query.text)
    assert text == 'Resume Builder'

@allure.feature("Resume Builder RB_UI 1.2")
@allure.story("Check Create Resume Button")
@pytest.mark.ui
@pytest.mark.smoke
def test_create_resume_button_functionality(login):
    page = ResumeBuilderPage()
    page.open_resume_builder_page()
    page.click(RB_Loc.CREATE_NEW_RESUME_BUTTON)
    assert page.should_have_title('Jobsolv | Create New Resume'), "Opened page has improper title"


@allure.feature("Resume Builder RB_UI 1.3")
@allure.story("Check Tailor Resume Button")
@pytest.mark.ui
@pytest.mark.smoke
def test_tailor_resume_button_functionality(login):
    page = ResumeBuilderPage()
    page.open_resume_builder_page()
    page.click(RB_Loc.TAILOR_RESUME_BUTTON)
    assert page.should_have_title('Jobsolv | Tailor Resume'), "Opened page has improper title"

@allure.feature("Resume Builder RB_UI 1.4")
@allure.story("Check Resumes List")
@pytest.mark.ui
@pytest.mark.smoke
def test_verify_my_resumes_list(login):
    page = ResumeBuilderPage()
    page.open_resume_builder_page()
    headers = ss(RB_Loc.TABLES_HEAD)
    expected_headers = ["Name", "Status", "Last edited", "Actions"]
    actual_headers = [header.get(query.text) for header in headers]
    assert actual_headers == expected_headers, f"Table columns heads are wrong: {actual_headers}"
    rows = ss(RB_Loc.ROWS)
    if len(rows) == 0:
        warnings.warn("There are no items in the table to check! My Resume Table verification is missed")
    assert len(rows) <= 10, "Invalid number of rows in the My Resume table"
    table = s(RB_Loc.TABLE)
    assert table.should(be.visible), "Table is not visible on the page"


@allure.feature("Resume Builder RB_UI 1.5")
@allure.story("Pagination Navigation")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.pagination
def test_pagination(login):
    page = ResumeBuilderPage()
    page.open_resume_builder_page()
    page_indicator = s(RB_Loc.PAGE_INDICATOR).get(query.text)
    current_page = page_indicator.split()[1]
    logger.info(f'current page is: {current_page}')
    total_pages = page_indicator.split()[3]
    logger.info(f'total pages is: {total_pages}')
    assert int(current_page) == 1, "Current page should be 1 on initial load"
    assert int(total_pages) >= 1, "Total pages should be greater or equal to 1"

    if total_pages == 1:
        warnings.warn("There is only one page! My Resume Table pagination verification is missed")

    # Check Back Button is unavailable on the first page
    back_button = s(RB_Loc.PAGINATION_BACK)
    assert back_button.should(have.attribute('disabled')), "Back button should be disabled on the first page"

    # Navigate to the second page
    page.click(RB_Loc.PAGINATION_NEXT)
    updated_page = s(RB_Loc.PAGE_INDICATOR).get(query.text).split()[1]
    assert int(updated_page) == 2, "Current page should be 2 after navigating forward"

    # Navigate to the last page
    while int(updated_page) < int(total_pages):
        page.click(RB_Loc.PAGINATION_NEXT)
        updated_page = s(RB_Loc.PAGE_INDICATOR).get(query.text).split()[1]

    assert int(updated_page) == int(total_pages), "Current page should match total pages on the last page"

    # Check the Next button is unavailable on the last page
    forward_button = s(RB_Loc.PAGINATION_NEXT)
    assert forward_button.should(have.attribute('disabled')), "Forward button should be disabled on the last page"

    # Navigate back to the first page
    while int(updated_page) > 1:
        page.click(RB_Loc.PAGINATION_BACK)
        updated_page = s(RB_Loc.PAGE_INDICATOR).get(query.text).split()[1]

    assert int(updated_page) == 1, "Current page should be 1 after navigating back to the first page"


