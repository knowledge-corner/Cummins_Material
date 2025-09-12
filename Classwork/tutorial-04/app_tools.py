from crewai.tools import tool
import requests
from dotenv import load_dotenv
import os


load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@tool("Fetch Shipment Details")
def get_shipment_details_tool(consignment_id : str) -> dict:
    """Fetch shipment details by consignment ID from a JSON API."""

    response = requests.get(rf"{BASE_URL}/api/shipments/{consignment_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch shipment details"}
    

# consignment_id = "JAI-00001"
# print(get_shipment_details_tool(consignment_id))