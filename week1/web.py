import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

# A class to represent a Webpage
# If you're not familiar with Classes, check out the "Intermediate Python" notebook

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self,url):
        
        '''
        Create the website object from the give url
        using the Beautiful Soup library
        '''
        self.url = url 
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.content,'html.parser')
        self.title = soup.title.string if soup.title else "No title found"

        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

    def get_contents(self):

        return f"Webpage Title: \n{self.title}\n Webpage "



# web = Website("https://edwarddonner.com")
# print(web.title)
# print(web.text)
