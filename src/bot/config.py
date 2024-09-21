import os

from dotenv import load_dotenv

load_dotenv()

TG_token = os.getenv('TG_TOKEN')

INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/")
