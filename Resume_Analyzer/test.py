from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = [
    "gemini-2.5-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-1.5-pro-002"
]

for model in models:
    print(f"\nTrying {model}")

    try:
        response = client.models.generate_content(
            model=model,
            contents="Say hello in one sentence."
        )
        print("✅ SUCCESS")
        print(response.text)
        break
    except Exception as e:
        print("❌", e)