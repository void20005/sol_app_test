from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Base URL for the application
BASE_URL = os.getenv('BASE_URL')

# Credentials for login
USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')

# Google account credentials (if needed for other tests)
GOOGLE_EMAIL = os.getenv('GOOGLE_EMAIL')
GOOGLE_PASSWORD = os.getenv('GOOGLE_PASSWORD')
