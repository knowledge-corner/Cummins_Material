# All inputs - 

from dotenv import load_dotenv
import os
from groq import Groq
import gradio as gr

# Load the API keys from .env file
load_dotenv(override=True)
key = os.getenv("GROQ_API_KEY")

def chat(prompt, history):

    message = [{"role": "user", "content": prompt},
               {"role": "system", "content": "You are a high teacher."}]
    
    client = Groq(api_key = key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=message
    )

    reply = response.choices[0].message.content
    return reply

# Create Gradio interface to interact with the chat function
gr.ChatInterface(fn=chat, type = "messages").launch()
