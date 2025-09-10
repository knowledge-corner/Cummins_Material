from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os
import gradio as gr

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

class PDFChatAgent:

    def __init__(self, pdf_path = None):
        if pdf_path:
            read_pdf = PdfReader(pdf_path)
            self.text = "\n".join(page.extract_text() for page in read_pdf.pages)
        else:
            self.text = ""


    def system_prompt(self):
        
        prompt = f"""
        You are a helpful assistant who can read and understand the content of a PDF document.
        The content of the PDF is as follows: {self.text}. 
        Answer the user's questions based on the content of the PDF.
        If you dont know the answer, just say that you don't know, don't try to make up an answer.
        Question is - """

        return prompt

    def chat(self, question, history):
        client = OpenAI(api_key=key)

        messages = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": question}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        answer = response.choices[0].message.content
       
        return answer
    
if __name__ == "__main__":
    pdf_path = "profile.pdf"  
    agent = PDFChatAgent(pdf_path)
    gr.ChatInterface(
        fn=agent.chat, type = "messages", title="PDF Chatbot",).launch()


