# sol_app_test

A comprehensive automated testing project for a web application, leveraging **Pytest**, **Selene**, **Requests** and **Allure** for seamless testing and reporting.

---

## Features

- **Page Object Model (POM)**: A clean structure to organize locators and methods for web pages.
- **Allure Reporting**: Generate user-friendly, detailed reports for test results.
- **Environment Configuration**: Use a `.env` file to manage sensitive data, such as URLs, emails, and passwords.
- **Pytest Framework**: Lightweight and scalable for various testing needs.
- **API Testing**: API testing with Request library
- **Integration testing**: UI & API

### **Installation (Linux, Mac, Win):**
```
git clone git@github.com:void20005/sol_app_test.git
cd sol_app_test
```
#### Create .env file with variables like:
```
BASE_URL=https://your-web-app-url.com
BASE_URL_API=https://your-web-app-url-api.com
USER_EMAIL=your-email@example.com
USER_PASSWORD=your-password
GOOGLE_EMAIL=your-google-email@example.com
GOOGLE_PASSWORD=your-google-password
```
#### If you prefer to use venv:
#### Linux\Mac
```
python -m venv venv
source venv/bin/activate
```
#### Win
```

python -m venv venv
venv\Scripts\activate
```
#### Install requirements:

```
pip install -r requirements.txt
```

### RUNNING TESTS


#### Collecting tests:
```
python -m pytest --co
```

#### Run specified test:
```
python -m pytest -k <test_name>
```

#### Example:
```
python -m pytest -k test_successful_login
```

#### Run all tests:
```
python -m pytest
```
#### Run only API tests:
```
python pytest -m api
```
#### Run only smoke tests:
```
python pytest -m smoke
```

#### Run only regression  tests:
```
python pytest -m regression 
```

#### Run only integration tests:
```
python pytest -m integration
```

#### Run all tests with allure report:
```
pytest --alluredir=allure-results
```
#### Generate and serve Allure report (opens in a browser automatically):
```
allure serve allure-results
```
#### Generate and save Allure report without serving:
```
allure generate allure-results -o allure-report
```

#### Tools and Technologies
```
Python 3.8+
Pytest: Test framework for efficient testing.
Selene: A wrapper for Selenium for simplified web element interactions.
Allure: A powerful tool for generating advanced test reports.
Requests: A library for making HTTP requests, enabling robust API testing.
```
```
