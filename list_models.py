import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

print("Listing available models:")
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(f"- {m.name}")
