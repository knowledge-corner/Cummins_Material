#pip install langgraph
#pip install langchain_groq
#pip install langchain_openai
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from app_tools import get_shipment_details_tool

load_dotenv()
# Define LLM
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    api_key=os.getenv("API_KEY")
)

# Define States
class Consignement(dict):
    consignment_id: str
    status: str
    message: str

# Function Node or Tool Node
def get_shipment_details(consignment: Consignement) -> Consignement:
    """Fetch shipment details by consignment ID from a JSON API."""

    consignment_id = consignment['consignment_id']
    result = get_shipment_details_tool(consignment_id)
    consignment['status'] = result.get('status', 'Unknown') 
    return consignment  

# LLM Node
def summarize_status(consignment: Consignement) -> Consignement:
    """Summarize the shipment status using LLM."""

    prompt = f"Summarize the following shipment status as a message: {consignment['status']}"
    summary = llm.invoke(prompt)
    consignment['message'] = summary.content

    return consignment

# Build Graph

graph = StateGraph(Consignement)

# add nodes
graph.add_node("GetShipmentDetails", get_shipment_details)
graph.add_node("SummarizeStatus", summarize_status)

# add edges
graph.set_entry_point("GetShipmentDetails")
graph.add_edge("GetShipmentDetails", "SummarizeStatus")
graph.add_edge("SummarizeStatus", END)

# Compile the graph
app = graph.compile()

# Run the graph - main
if __name__ == "__main__":
    consignment_id = "JAI-00001"
    initial_state = Consignement(consignment_id=consignment_id, status="", message="")
    final_state = app.invoke(initial_state)
    print(final_state["message"])
