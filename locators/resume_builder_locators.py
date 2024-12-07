class ResumeBuilderLocators:
    CREATE_NEW_RESUME_BUTTON = '//a[@href="/create-resume"]'
    TAILOR_RESUME_BUTTON = '//a[@href="/upload-resume"]'
    TABLE = 'table.w-full.caption-bottom.text-sm'
    TABLES_HEAD = '//table//thead/tr/th'
    ROWS = '//table/tbody/tr'
    ROW_ACTION_BUTTON = './/td[last()]//button'
    GRID_VIEW_BUTTON = '//button[@aria-label="grid"]'
    LIST_VIEW_BUTTON = '//button[@aria-label="list"]'
    PAGE_NAME_TEXT = '//h2[contains(@class, "text-text1")]'
    PAGINATION_BACK = 'nav[aria-label="pagination"] button:first-of-type'
    PAGINATION_NEXT = 'nav[aria-label="pagination"] button:last-of-type'
    PAGE_INDICATOR = '//nav/ul/li[1]/span'

