from dotenv import load_dotenv
from openai import OpenAI
import os
from rich.markdown import Markdown
from rich.console import Console

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

prompt = "What is factorial of a number?"
message = [{"role": "user", "content": prompt},
           {"role": "system", "content": "You are a high teacher."}]

# openai_obj = OpenAI(api_key=key)

# response = openai_obj.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=message
# )

# print(response.choices[0].message.content)

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=message
)
result = response.choices[0].message.content
console = Console()
console.print(Markdown(result))

# Gemini 1.5 Turbo

# from google import genai

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# response = client.models.generate_content(
#     model="gemini-1.5-turbo",
#     contents=prompt
# )
# print(response.choices[0].message.content)
