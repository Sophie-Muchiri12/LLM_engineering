#chat completions api
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("No api key was found")
else:
    print("API key was found!")

openai=OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type":"application/json"
    
    }


payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [{
        "role":"user",
        "content":"Tell me a fun fact"
    }]
}


