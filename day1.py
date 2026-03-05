import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI


#connecting to OpenApi or Ollama

# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')


openai=OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)
#Making a quick call to openAi

message = "Hello, GPT! This is my first ever message to you"
response = openai.chat.completions.create(

    model="llama-3.1-8b-instant",
    messages=[{
        "role":"user",
        "content":message
    }]
)
print(response)
# print(response.choices[0].message.content)