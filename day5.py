from linksite import Website
# imports
# If these fail, please check you're running from an 'activated' environment with (llms) in the command prompt

import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI


#load environment variable
load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')

#instantiate the OpenAI class with apikey and base url
openai = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

#system prompt
link_system_prompt = "You are provided with a list of link found in a webpage\n" \
"You are able to decide which of the links would be most relevant to include in the brochure aboutthe company\n" \
"such as links to an About page,or company page or careers page\n "

link_system_prompt += "You should respond in JSON: "

link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

print(link_system_prompt)

weburl1 = Website("https://edwarddonner.com")
#user prompt function
def get_links_user_prompt(weburl):
    user_prompt = f"Here is the list of links on the website of {weburl} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(weburl.links)
    return user_prompt

print(get_links_user_prompt(weburl1))
