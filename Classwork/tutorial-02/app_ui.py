from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import os
from google import genai
from groq import Groq

# Load environment variables (expects OPENAI_API_KEY in .env)
load_dotenv(override=True)

print("PDFChatAgent class is defined")
class PDFChatAgent:
    def __init__(self, pdf_path, summary_path= "documents/summary.txt"):

        # Load PDF text
        self.pdf_text = ""
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.pdf_text += text


    def system_prompt(self):
        print("generating System prompt")
        prompt = (
            f"## PDF Content:\n{self.pdf_text}\n\n"
            f"## Summary:\n{self.summary}\n\n"
            "You are a helpful assistant who can read candidate details from the PDF context and Summary"
            "You must answer the following question based on the context provided and \n"
            "If the context does not provide the answer, respond with 'I don't know.'\n"
            )
        return prompt
      
    def groq_model(self, prompt):
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=prompt)           

        print("Response is generated using groq model")
        return response.choices[0].message.content

    def openai_model(self, prompt):
        response = OpenAI().chat.completions.create(    # works, because load_dotenv put the key into env
            model="gpt-4o-mini",
            messages=prompt)

        print("Response is generated using openai model")
        return response.choices[0].message.content
    
    def gemini_model(self, prompt):
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt[0].get("content"))

        print("Response is generated using gemini model")
        return response.text
    
    def ollama_model(self, prompt):
        ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
        model_name = "llama3.2"

        response = ollama.chat.completions.create(
            model=model_name,
            messages=prompt)

        print("Response is generated using ollama model")
        return response.choices[0].message.content

    def chat(self, prompt, history):
        messages = [{"role": "system", "content":  self.system_prompt() + prompt}]
        
        # response_text = self.openai_model(messages)
        # response_text = self.groq_model(messages)
        response_text = self.gemini_model(messages)   
        # response_text = self.ollama_model(messages)

        return response_text

# Gradio with CSS Launch mode - -------------------------------------

# Custom CSS for UI enhancements
custom_css = """
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f8f9fa;
}
.gradio-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
}
.message.user {
    background-color: #e3f2fd;
    border-radius: 8px;
    padding: 10px;
}
.message.bot {
    background-color: #fff3e0;
    border-radius: 8px;
    padding: 10px;
}
"""

# Initialize and launch the Gradio app
if __name__ == "__main__":
    agent = PDFChatAgent("profile.pdf")
    gr.ChatInterface(
        agent.chat,
        title="📄 Resume Scanner",
        theme="soft",
        css=custom_css,
        textbox=gr.Textbox(
            placeholder="Ask about the candidate's experience, skills, etc.",
            show_copy_button=True
        ),
        type="messages"
    ).launch(share=True)
