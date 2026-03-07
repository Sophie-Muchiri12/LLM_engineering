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



OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "phi3"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type":"application/json"
    
    }


payload = {
    "model": "phi3",
    "messages": [{
        "role":"user",
        "content":"Tell me a fun fact"
    }],
    "stream":False
}

response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
print(response.json()['message']['content'])
# print(response.json())



