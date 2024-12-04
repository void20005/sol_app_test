class LoginLocators:
    EMAIL = '//form//input[@type="email"]'
    PASSWORD = '//form//input[@type="password"]'
    LOGIN_BUTTON = '//form//button[@type="submit"]'
    FORGET_PASSWORD_BUTTON = '//form//a[@href="/auth/forget-password"]'
    GOOGLE_LOGIN_BUTTON = '//form//a[contains(text(), "Sign in with Google")]'
    SIGN_UP_BUTTON = '//form//a[@href="/auth/sign-up"]'
    MAIN_PAGE_SIGN_OUT_BUTTON = '//button[@aria-label="Sign out"]'
