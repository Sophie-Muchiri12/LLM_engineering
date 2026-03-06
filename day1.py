import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI
from week1.web import Website

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
# print(response)
# print(response.choices[0].message.content)

#instantiate web oblect
web = Website("https://campusbiz.co.ke/careers/vacancy/869374-interintel-technologies-site-reliability-engineer-intern-nairobi/amp/")

# **A system prompt** that tells them what task they are performing and what tone they should use

# **A user prompt** -- the conversation starter that they should reply to

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

#A function that writes a User prompt that asks for a summary of websites:

def user_prompt(websiteurl):
    user_prompt = f"You are looking at a website titled {websiteurl.title}"
    user_prompt += "\n The contents of the website is as follows:\nplease provide a short sumary of the website in markdown\n"
    user_prompt += websiteurl.text
    return user_prompt

print(user_prompt(web))

'''
The API from OpenAI expects to receive messages
in a particular structure.Many of the other
APIs share this structure

    [
        {"role":"system", "content":"system message goes here"},
        {"role":"user", "content":"user message goes here"}
    ]
'''

#Example
messages = [
    {"role": "system", "content": "You are a snarky assistant"},
    {"role": "user", "content": "What is 2 + 2?"}
]

#Using the chat completion model with system and user message
response2 = openai.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages = messages
)

print(response2.choices[0].message.content)


#The same format but via a function

def message_for(websiteurl):
    # Return a properly formatted messages list: one system message and one user message
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt(websiteurl)}
    ]

# print(message_for(web))


#A function that summarize it all

def sumarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages = message_for(website)
    )
    return response.choices[0].message.content

print(sumarize("https://edwarddonner.com"))