import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyDPqFPrH3AlMZyC1XaREjwztJZPfbNuBoA"

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
    print("Done listing.")
except Exception as e:
    print(f"Error listing models: {e}")
