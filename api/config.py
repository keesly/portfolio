from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Constants for the application
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_API_URL = os.getenv("GITHUB_API_URL")
FE_DOMAIN = os.getenv("FE_DOMAIN")
API_URL = os.getenv("API_URL")

# Print for debugging
print(f"GITHUB_API_URL: {GITHUB_API_URL}")
print(f"GITHUB_USERNAME: {GITHUB_USERNAME}")