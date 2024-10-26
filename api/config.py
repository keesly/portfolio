from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Constants for the application
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_API_URL = os.getenv("GITHUB_API_URL")