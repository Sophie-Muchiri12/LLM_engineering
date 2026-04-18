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

system_prompt = 'You are a helpful assistant that responds in markdown without code block'

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
    fn=messages, #callback function
    inputs="textbox",
    outputs="textbox"
).launch(inbrowser=True)

message_input = gr.Textbox(
    label="Your message: ",
    info="Enter a message for Groq",
    lines=7
    
    )

message_output = gr.Markdown(
    label="Groq response"
)


# view = gr.Interface(
#     fn=messages,
#     title="Groq",
#     inputs=[message_input],
#     outputs=[message_output]
# )

# view.launch(inbrowser=True)


# wanting gradio to respond in markdown

markdown_view = gr.Interface(
    fn=messages,
    title="Groq",
    inputs=[message_input],
    outputs=[message_output],
    examples=[
        "Explain the Transformer architecture to a layperson"
        "Explain the Transformer architecture to an aspiring  AI Engineer"
    ],
    flagging_mode="never"
)

markdown_view.launch()

#streaming - generator with gradio