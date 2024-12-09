from locators.base_locators import BaseLocators


class EditResumeLocators(BaseLocators):
    RESUME_NAME_FIELD = 'span[class*="text-base font-normal text-text5 truncate"]'