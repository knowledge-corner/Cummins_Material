from crewai import Crew, Agent, Task, LLM
from dotenv import load_dotenv
from app_tools import *
import os

load_dotenv()

# Assign LLM
my_llm = LLM(
    model=os.getenv("MODEL"), 
    api_key=os.getenv("API_KEY")
)

# Define Agent
email_agent = Agent(
   name="email_agent",
    role="Logistics Support Specialist",
    goal="Identify emails asking for shipment status and extract the consignment ID.",
    backstory="You work in a shipping company and help customers by checking if an email is about a consignment status request.",
    llm=my_llm,
    verbose=True,
    tools=[get_unread_emails_tool]
)


shipment_agent = Agent(
    name="ShipmentAgent",
    role="Logistic Manager",
    goal = "Fetch and summarize shipment details using JSON API.",
    backstory="You have access to a tool that fetches shipment details by consignment ID.",
    llm=my_llm,
    tools=[get_shipment_details_tool]
)

# Define Task

fetch_email_task = Task(
    name="FetchEmailTask",
    description='''You are given a list of emails (with subject and body).
    For each email:
    1. Read the subject and body.
    2. Decide if it is asking for consignment/shipment/ID status.
    3. If yes, extract the consignment_id (alphanumeric or numeric).
    4. Consolidate all details from all emails as JSON with subject, consignment_id and sender email.
    Output results as a JSON list like:
    [{"subject": "...", "consignment_id": "...", "from" : "..."}]''',
    expected_output="List of consignment IDs extracted from emails.",
    agent=email_agent,
    output_file = "consignment_ids.json"
)

fetch_shipment_task = Task(
    name="FetchShipmentTask",
    description="Fetch shipment status by consignment ID extracted by email agent and summarize the details.",
    expected_output="Consignment ID and status summary in a sentence format.",
    agent=shipment_agent,
)

crew = Crew(
    name="ShipmentCrew",
    agents=[email_agent, shipment_agent],
    tasks=[fetch_email_task, fetch_shipment_task]
)

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)