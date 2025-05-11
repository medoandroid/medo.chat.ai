import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def chat_with_gemini(messages):
    text_history = [msg["content"] for msg in messages if msg["role"] == "user"]
    prompt = "\n".join(text_history)
    response = model.generate_content(prompt)
    return response.text
