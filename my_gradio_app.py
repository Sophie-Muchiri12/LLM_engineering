import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
# import anthropic

import gradio as gr

load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')

#instantiate the openai class

openai = OpenAI(
    api_key=api_key,
    base_url='https://api.groq.com/openai/v1'
)

system_prompt = 'You are a helpful assistant'

def messages(prompt):

    messages = [
        {"role":"system", "content":system_prompt},
        {"role":"user", "content":prompt}

    ]

    response = openai.chat.completions.create(
        model = 'llama-3.1-8b-instant',
        messages=messages
    )

    return response.choices[0].message.content


# print(messages("What is today's date?"))


#responses api is more better than chat completions api

def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

shout("Hello!")

gr.Interface(
    fn=shout,
    inputs="textbox",
    outputs="textbox"
).launch(inbrowser=True)