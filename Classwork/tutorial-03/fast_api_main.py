from app_crew import crew
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def run_crew(description):
    result = crew.kickoff(inputs={"requirements": description})
    return result.tasks_output[0]  # Output of coding task


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_code(description: str = Form(...)):
    result = run_crew(description)
    return HTMLResponse(content=f"<h2>Generated Code:</h2><pre>{result}</pre>")

uvicorn.run(app, host="127.0.0.1", port=8000)