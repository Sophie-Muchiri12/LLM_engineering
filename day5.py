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
import json

#load environment variable
load_dotenv(override=True)
api_key = os.getenv('GROQ_API_KEY')

#instantiate the OpenAI class with apikey and base url
openai = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.1-8b-instant"

# system prompt

link_system_prompt = """
You are provided with links from a webpage.

Select links relevant for a company brochure such as:
- About
- Careers
- Company
- Blog
- Documentation

Return STRICT JSON.

Each object MUST contain:
"type"
"url"

Example:

{
  "links": [
    {"type": "about", "url": "https://example.com/about"},
    {"type": "careers", "url": "https://example.com/careers"}
  ]
}
"""
# print(link_system_prompt)

#user prompt function
weburl1 = Website("https://edwarddonner.com")

def get_links_user_prompt(weburl):
    user_prompt = f"Here is the list of links on the website of {weburl} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(weburl.links)
    return user_prompt

# print(get_links_user_prompt(weburl1))

# function that will handle the completions model to get the links\n via the  model +system prompt + user prompt

# the difference btw the website class and the get links function is that the function filters links that are related to the site(via chat model) 
# while the website class retrieves all links whether related to the site or not


def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)

# print(get_links("https://huggingface.co"))


## Now we have to make the brochure

def get_contents_and_links(weburl):
    #Instantiate the website class to utilize the get_content instance method

    webby = Website(weburl)
    print(f"The Landing page of:\n")

    #Using the get_links ai method we get all the related absolute links to the site
    links = get_links(weburl)
    # print(json.dumps(links, indent=4))
    
    result = webby.get_contents()

    #looping through the links object
    for link in links['links']:
        '''
        we then are inside the lists of objects of page type(eg:career pages) and url\n 
        we would want to obtain the url then pass it to the website class so that 
        it also exxtracts the content of that webpage
        '''
        try:
            url = link.get("url")
            link_type = link.get("type", "related page")

            print("Reading:", url)

            result += f"\n\n{link_type}\n"
            result += Website(url).get_contents()

        except Exception as e:
            print("Skipping link:", link.get("url"))
            print("Reason:", e)

    return result

  




# print(get_contents_and_links("https://huggingface.com"))

'''
IN SUMMARY THE get_contents_and_links function gets all the contents of a single page
including the contents of related pages 

What we need now is a system prompt that  will instruct to make a brochure from the contents
retrieved by get_contents_and_links function
'''

#system prompt:

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

#user prompt to feed the response chat completion our get_contents_and_links function

def get_user_prompt_brochure(companyname,weburl):
    user_prompt = f"You are looking at a company called {companyname}"
    user_prompt += f"So here is the content of the webpage with its relevant pages\n use this information to build a short brochure of the company in markdown"
    user_prompt += get_contents_and_links(weburl)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt


'''
Now we create the fuunction that will help calling
the ai to help us make the brochure
'''

def create_brochure_openai_call(companyname,url):
    response = openai.chat.completions.create(
        model = MODEL,
        messages = [
            {"role":'system', "content":system_prompt},
            {"role":"user", "content":get_user_prompt_brochure(companyname,url)}
        ]
    )
    result = response.choices[0].message.content
    print(result)


create_brochure_openai_call("Ed donner", "https://edwarddonner.com")