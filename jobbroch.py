import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import json

# Retrieving keys from .env
load_dotenv(override=True)
api_key = os.get('GROQ_API_KEY')

#Instantiate openai object with key and baseurl
openai = OpenAI(
    api_key=api_key,
    baseurl='https://api.groq.com/openai/v1'
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
1 link_system_prompt - direct llm to scrape links related to job seekers
2 user_link_prompt - provide the llm the website url and direct it to do the same
3 get_link function - will use the link_system_prompt and user_link_prompt
4 get_content_link function - will fetch the content of site and all links using get_link function
5 job_brief_system_prompt - direct llm to create a job seeking briefing based on the url that the user will provide
6 user_job_url_prompt - passes the url of interest to the get_content_link function to obtain all contents & links 
    related to the job seeker and will ask the llm to create the briefing out of the contents provided


'''

