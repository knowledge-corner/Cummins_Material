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
shipment_agent = Agent(
    name="ShipmentAgent",
    role="Logistic Manager",
    goal = "Fetch and summarize shipment details using JSON API.",
    backstory="You have access to a tool that fetches shipment details by consignment ID.",
    llm=my_llm,
    tools=[get_shipment_details_tool]
)

# Define Task
fetch_shipment_task = Task(
    name="FetchShipmentTask",
    description="Fetch shipment status by {consignment_id} and summarize the details.",
    expected_output="Consignment ID and status summary as a Json file.",
    agent=shipment_agent,
    output_file = "details.json"
)

crew = Crew(
    name="ShipmentCrew",
    agents=[shipment_agent],
    tasks=[fetch_shipment_task]
)

if __name__ == "__main__":
    consignment_id = "JAI-00001"
    crew.kickoff(inputs = {"consignment_id": consignment_id})