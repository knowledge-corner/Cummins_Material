from crewai.tools import tool
import requests
from dotenv import load_dotenv
import os


load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@tool("Fetch Shipment Details")
def get_shipment_details_tool(consignment_id):
    """Fetch shipment details by consignment ID from a JSON API."""

    response = requests.get(rf"{BASE_URL}/api/shipments/{consignment_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch shipment details"}
    

@tool("Get Unread Emails")
def get_unread_emails_tool():
    """Fetch unread emails from a specified Outlook inbox using Microsoft Graph API."""

#     authority = f"https://login.microsoftonline.com/{os.getenv('tenant_id')}"
#     scope = ["https://graph.microsoft.com/.default"]

#     app = msal.ConfidentialClientApplication(
#         client_id=os.getenv("client_id"),
#         client_credential=os.getenv("client_secret"),
#         authority=authority
#     )

#     result = app.acquire_token_for_client(scopes=scope)
#     if "access_token" not in result:
#         raise Exception("Could not obtain token: ", result)

#     access_token = result["access_token"]

# # ------------------ Fetch Emails ------------------
#     url = (
#         "https://graph.microsoft.com/v1.0/"
#         "users/vaidehi.nair@knowledgecorner.in/mailFolders/inbox/messages"
#         "?$filter=isRead eq false"
#     )
#     headers = {"Authorization": f"Bearer {access_token}"}

#     response = requests.get(url, headers=headers)
#     messages = response.json().get("value", [])

    # emails = [
    #     {"subject": msg["subject"], 
    #     "body": msg.get("body", {}).get("content", ""),
    #     "from": msg.get("from", {}).get("emailAddress", {}).get("address", "")}
    #     for msg in messages
    # ]
    emails = [{'subject': 'shipment status', 'body': '<html><head>\r\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body><div dir="ltr"><div>what is update on&nbsp;the shipment -&nbsp;<span style="color:rgb(0,0,0)">JAI-00001?</span></div><div><br></div><div><br></div><div><div dir="ltr" class="gmail_signature" data-smartmail="gmail_signature"><div dir="ltr"><p class="MsoNormal"><b><span style="font-size:12.0pt; font-family:Mali; color:#333f50">Vaidehi Nair</span></b></p><p class="MsoNormal"><span style="font-family:Mali; color:#333f50"><br></span></p><p class="MsoNormal"><span style="color:rgb(51,63,80); font-family:Mali">Knowledge Corner</span><span style="font-family:Mali; color:#333f50"><br></span><span style="font-size:9.0pt; font-family:Mali; color:#333f50">Corporate Trainer | Tableau | Python | Power BI<br>Mob: +91 9664353290</span></p><p class="MsoNormal"><span style="font-size:9.0pt; font-family:Mali; color:#333f50"><a href="http://bit.ly/vaidehinair" target="_blank">YouTube Channe</a>l |&nbsp;</span><span style="color:rgb(51,63,80); font-family:Mali; font-size:9pt"><a href="http://bit.ly/vaidehinair_linkedin" target="_blank">LinkedIn</a></span></p></div></div></div></div></body></html>', 'from': 'vaidehi89@gmail.com'}]
    return emails
    

# consignment_id = "JAI-00001"
# print(get_shipment_details_tool(consignment_id))