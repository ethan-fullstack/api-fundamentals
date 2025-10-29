import requests

import os
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DIRECTUS_URL", "").rstrip("/")

url = f"{BASE_URL}/products"

print(f"GET {url}")

response = requests.get(url)

print(response.json())
