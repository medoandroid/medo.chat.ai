import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content
