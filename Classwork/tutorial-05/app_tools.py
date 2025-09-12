import requests
import msal
from dotenv import load_dotenv
import os
from crewai.tools import tool 

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@tool("Fetch Shipment Status")
def fetch_shipment_status_tool(consignment_id: str):
    '''Fetch shipment status from the JSON API given a consignment ID.'''
    URL = rf"{BASE_URL}/api/shipments/{consignment_id}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": f"Failed to fetch status for {consignment_id}"}
    
@tool("Get Unread Emails")
def get_unread_emails_tool():
    """Fetch unread emails from a specified Outlook inbox using Microsoft Graph API."""

    authority = f"https://login.microsoftonline.com/{os.getenv('tenant_id')}"
    scope = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(
        client_id=os.getenv("client_id"),
        client_credential=os.getenv("client_secret"),
        authority=authority
    )

    result = app.acquire_token_for_client(scopes=scope)
    if "access_token" not in result:
        raise Exception("Could not obtain token: ", result)

    access_token = result["access_token"]

# ------------------ Fetch Emails ------------------
    url = (
        "https://graph.microsoft.com/v1.0/"
        "users/vaidehi.nair@knowledgecorner.in/mailFolders/inbox/messages"
        "?$filter=isRead eq false"
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    messages = response.json().get("value", [])

    emails = [
        {"subject": msg["subject"], 
         "body": msg.get("body", {}).get("content", ""),
         "from": msg.get("from", {}).get("emailAddress", {}).get("address", "")}
        for msg in messages
    ]

    return emails

@tool("Send Status Update Email")
def send_email_tool(recipient: str, subject: str, body: str):
    """Send an email using Microsoft Graph API."""
    authority = f"https://login.microsoftonline.com/{os.getenv('tenant_id')}"
    scope = ["https://graph.microsoft.com/.default"]

    # Authenticate
    app = msal.ConfidentialClientApplication(
        client_id=os.getenv("client_id"),
        client_credential=os.getenv("client_secret"),
        authority=authority
    )
    result = app.acquire_token_for_client(scopes=scope)
    if "access_token" not in result:
        raise Exception("Could not obtain token: ", result)

    access_token = result["access_token"]

    # Build email payload
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": recipient}}
            ]
        },
        "saveToSentItems": "true"
    }

    # Send email
    url = "https://graph.microsoft.com/v1.0/users/{}/sendMail".format(
        os.getenv("sender_email")  # must be a licensed mailbox in your tenant
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=email_msg)
    if response.status_code == 202:
        return {"status": "success", "message": f"Email sent to {recipient}"}
    else:
        return {"status": "error", "details": response.json()}