import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get("models", [])
    for m in models:
        methods = m.get("supportedGenerationMethods", [])
        if "embedContent" in methods or "batchEmbedContents" in methods:
            print(m['name'])
else:
    print(f"Error: {response.status_code} - {response.text}")
