from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Base URL for the application
BASE_URL = os.getenv('BASE_URL')
BASE_URL_API = os.getenv('BASE_URL_API')

# Credentials for login
USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')

# Google account credentials (if needed for other tests)
GOOGLE_EMAIL = os.getenv('GOOGLE_EMAIL')
GOOGLE_PASSWORD = os.getenv('GOOGLE_PASSWORD')

# Path to test data
PATH_DATA = os.getenv('PATH_DATA')

# Responses
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
STATUS_UNPROCESSABLE_ENTITY = 422
