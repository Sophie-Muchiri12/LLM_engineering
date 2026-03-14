import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import json
from linksite import Website

# Retrieving keys from .env
load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')

#Instantiate openai object with key and baseurl
openai = OpenAI(
    api_key=api_key,
    base_url='https://api.groq.com/openai/v1'
)

#set up model to use
model = 'llama-3.1-8b-instant'

'''
WORK FLOW:
- We need to scrape content and links off of websites (generally)
    * website class scrapes all links and content 

    * for this im going to require a system & user prompts that deals specifically on filtering links
    that will be insightful to job seekers

- Creating the Job seeking brochure

    *for this i need a system & user prompts that will direct the llm to create a job seeking briefing
    for the job seeker based on the content collected

    * format the job seeking briefing as mark down

## Functions & variables to used
1 link_system_prompt - direct llm to scrape links related to job seekers [ :) ]
2 user_link_prompt function - provide the llm the website url and direct it to do the same [:)]
3 get_link function - will use the link_system_prompt and user_link_prompt and the ai to filter related links
4 get_content_link function - will fetch the content of site and all links using get_link function
5 job_brief_system_prompt - direct llm to create a job seeking briefing based on the url that the user will provide
6 user_job_url_prompt - passes the url of interest to the get_content_link function to obtain all contents & links 
    related to the job seeker and will ask the llm to create the briefing out of the contents provided


'''
# 1. link_system prompt

link_system_prompt = """
You are an assistant that analyzes a list of website links.

Your goal is to identify links that would be useful for a JOB SEEKER researching a company.

Select links related to:
- About the company
- Careers / Jobs
- Team
- Culture
- Engineering or Technology
- Blog or News
- Mission / Values

Ignore links related to:
- Privacy policy
- Terms of service
- Cookie policy
- Contact forms
- Social media (Twitter, LinkedIn, Facebook, Instagram)
- Login / Sign up pages

Return your answer as STRICT JSON dont put any trippl back ticks

Each item must contain:
"type" – the category of the page
"url" – the FULL https URL of the page

Example output:

{
  "links": [
    {"type": "about", "url": "https://example.com/about"},
    {"type": "careers", "url": "https://example.com/careers"},
    {"type": "engineering", "url": "https://example.com/engineering-blog"}
  ]
}
"""

# 2 user_link_prompt function

def get_user_link_prompt(url):
    web = Website(url)
    user_prompt = f"You are analyzing a company's website: {web}"
    user_prompt += '''
    Your task is to identify which links would be useful for a JOB SEEKER researching this company.

Select links related to:
- About
- Careers / Jobs
- Team
- Culture
- Engineering / Technology
- Blog / News
- Mission / Values

Here are the links found on the website:
    '''
    user_prompt += "\n".join(web.links)
    return user_prompt


# print(get_user_link_prompt("https://huggingface.co/"))

hugging_face = "https://huggingface.co/"
    
# 3 get_link function

def get_links(url):
    webby = Website(url)
    response = openai.chat.completions.create(
        model = model,
        messages = [
            {"role":"system", "content":link_system_prompt},
            {"role":"user", "content":get_user_link_prompt(url)}
        ]
    )
    result = response.choices[0].message.content

    print("RAW MODEL OUTPUT:")
    print(result)
    return json.loads(result)

print(get_links(hugging_face))