import os, json, re
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env safely with multiple encoding attempts
try:
    load_dotenv(encoding="utf-8")
except UnicodeDecodeError:
    try:
        load_dotenv(encoding="utf-8-sig")  # Try UTF-8 with BOM
    except UnicodeDecodeError:
        load_dotenv(encoding="latin-1")    # Fallback to Latin-1

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GENINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

genai.configure(api_key=API_KEY)

# Try different model names
try:
    # First try the newer model name
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("Using gemini-2.5-flash model")
except Exception as e:
    print(f"gemini-2.5-flash not available: {e}")
    try:
        # Try the original name
        model = genai.GenerativeModel("gemini-2.5-flash")
        print("Using gemini-pro model")
    except Exception as e2:
        print(f"gemini-2.5-flash not available: {e2}")
        # List available models
        try:
            models = genai.list_models()
            print("Available models:")
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            # Use the first available model that supports generateContent
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    model = genai.GenerativeModel(m.name)
                    print(f"Using available model: {m.name}")
                    break
            else:
                raise Exception("No models available with generateContent support")
        except Exception as e3:
            raise Exception(f"Could not list models: {e3}")

# Your function that uses the model
def ask_json(prompt, guard=""):
    try:
        resp = model.generate_content(prompt + guard)
        return resp.text
    except Exception as e:
        print(f"Error generating content: {e}")
        # Try with a simpler approach if the first fails
        try:
            resp = model.generate_content(prompt)
            return resp.text
        except Exception as e2:
            return f"Error: {str(e2)}"