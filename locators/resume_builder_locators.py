from importlib.metadata import pass_none

from past.translation import PastSourceFileLoader

from locators.base_locators import BaseLocators


class ResumeBuilderLocators(BaseLocators):
    CREATE_NEW_RESUME_BUTTON = '//a[@href="/create-resume"]'
    TAILOR_RESUME_BUTTON = '//a[@href="/upload-resume"]'
    TABLE = 'table.w-full.caption-bottom.text-sm'
    TABLE_GRID = 'div[class*="flex flex-row items-center justify-start flex-wrap gap-[20px] dark:bg-hover-dark"]'
    TABLES_HEAD = '//table//thead/tr/th'
    ROWS = '//table/tbody/tr'
    CELL_IN_ROW = './td[{index}]'
    ROW_ACTION_BUTTON = './/td[last()]//button'
    GRID_VIEW_BUTTON = '//button[@aria-label="grid"]'
    LIST_VIEW_BUTTON = '//button[@aria-label="list"]'
    PAGE_NAME_TEXT = '//h2[contains(@class, "text-text1")]'
    PAGINATION_BACK = 'nav[aria-label="pagination"] button:first-of-type'
    PAGINATION_NEXT = 'nav[aria-label="pagination"] button:last-of-type'
    PAGE_INDICATOR = '//nav/ul/li[1]/span'
    RESUME_ROW_MENU_EDIT_BUTTON = '//div[@role="menuitem" and .//span[text()="Edit"]]'
    RESUME_ROW_MENU_DELETE_BUTTON = '//div[@role="menuitem" and .//span[text()="Delete"]]'
    MODAL_TITLE = "//h2[contains(text(), 'Delete Resume?')]"
    MODAL_MESSAGE = "//p[contains(text(), 'Are you sure you want to delete this resume?')]"
    MODAL_DELETE_BUTTON = "//button[contains(text(), 'Delete')]"
    MODAL_CANCEL_BUTTON = "//button[contains(text(), 'Cancel')]"

