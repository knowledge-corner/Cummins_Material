from crewai import Agent, Task, Process, Crew, LLM
from dotenv import load_dotenv
from app_tools import *
import os

load_dotenv(override=True)  # Load environment variables from .env file

# Create a unified LLM instance
my_llm = LLM(
    model=os.getenv("MODEL"),   
    api_key=os.getenv("API_KEY"),
    temperature=0.7
)

# Defining Agents

# Shipment Agent - Handles shipment status and tracking
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
    name="shipment_agent",
    role="Shipment Status Tracker",
    goal="Read consignment IDs from emails and fetch their status. If the status is not found, respond with 'Status not found'. Format the output for all extracted shipments as 'The shipment id status is: <status>'.",
    backstory="Helps users track consignments by checking status from API. You're an expert in logistics and shipment tracking.",
    tools=[fetch_shipment_status_tool],
    verbose=True,
    llm=my_llm,
)

reply_agent = Agent(
    name="replay_agent",
    role="Shipment Notification Sender",
    goal=(
        "Read shipment statuses from the JSON file and send formatted emails "
        "to the original sender (using the 'from' field) with the latest status."
    ),
    backstory="You are responsible for notifying customers about shipment status updates.",
    llm=my_llm,
    tools=[send_email_tool],
)


# Defining Tasks

email_task = Task(
    name="email_analysis_task",
    description='''You are given a list of emails (with subject and body).
    For each email:
    1. Read the subject and body.
    2. Decide if it is asking for consignment/shipment status.
    3. If yes, extract the consignment_id (alphanumeric or numeric).
    4. Consolidate all details from all emails as JSON with subject, consignment_id and sender email.
    Output results as a JSON list like:
    [{"subject": "...", "consignment_id": "...", "from" : "..."}]''',
    agent=email_agent,
    expected_output="JSON list of status-request emails with consignment IDs."
)

get_shipment_status = Task(
    name="get_shipment_status",
    description="""Take the consignment IDs extracted from the email task 
    and fetch their latest shipment status and sender email details from the API.""",
    expected_output="JSON response with shipment status and sender email details for each consignment.",
    agent=shipment_agent,
    output_file="shipment_status.json" 
)

send_email_task = Task(
    name="send_shipment_emails",
    description="""For each record in the shipments JSON file generated in the previous task, 
        send an email to the 'from' address with the shipment ID and status.
        Format the email subject as: 'Update on your shipment <consignment_id>'
        Write a polite email body informing the recipient of their shipment status.""",
    expected_output="Confirmation of emails sent to each recipient.",
    agent=reply_agent,
)

# Defining Crew
crew = Crew(
    agents=[email_agent, shipment_agent, reply_agent],
    tasks=[email_task, get_shipment_status, send_email_task],
    process=Process.sequential
)