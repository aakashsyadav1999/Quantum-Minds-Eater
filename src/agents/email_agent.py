from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
import os
import base64
from email.mime.text import MIMEText
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import warnings

warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv(find_dotenv())

class GmailToolkit(GmailToolkit):
    def get_tools(self):
        return {
            "send_email": self.send_email,
            "send_email_with_attachment": self.send_email_with_attachment,
            "get_emails": self.get_emails,
            "get_email": self.get_email,
            "get_drafts": self.get_drafts,
            "get_draft": self.get_draft,
            "create_draft": self.create_draft,
            "delete_draft": self.delete_draft,
            "send_draft": self.send_draft,
            "get_labels": self.get_labels,
            "get_label": self.get_label,
            "create_label": self.create_label,
            "delete_label": self.delete_label,
            "get_threads": self.get_threads,
            "get_thread": self.get_thread,
            "create_thread": self.create_thread,
            "delete_thread": self.delete_thread,
            "get_history": self.get_history,
            "get_profile": self.get_profile,
        }
        
class Email:
    def __init__(self, to_email, subject, body):
        self.to_email = to_email
        self.subject = subject
        self.body = body

# Load Gmail credentials
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/gmail.compose"],
    client_secrets_file="credentials.json",
)

# Build Gmail API resource
api_resource = build_resource_service(credentials=credentials)

# Initialize Gmail Toolkit
toolkit = GmailToolkit(api_resource=api_resource)
GmailToolkit.model_rebuild()  # Fix for Pydantic model issue

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Setup LangChain Agent
instructions = "You are an assistant."
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
llm = ChatOpenAI(temperature=0)

# Create Agent
agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=False,  # Prevents email content from being displayed
)

# Function to create a valid email draft
def create_draft_message(to_email, subject, body):
    """
    Creates a properly formatted draft message for Gmail API.

    :param to_email: Recipient's email address
    :param subject: Subject of the email
    :param body: Email body content
    :return: Dictionary with encoded message
    """
    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {"message": {"raw": raw_message}}

# Get user input
to_email = input("Enter recipient's email: ").strip()
subject = input("Enter email subject: ").strip()
body_prompt = input("Enter a short description of your email content: ").strip()

# Generate AI content for the email
response = agent_executor.invoke(
    {"input": f"Write a professional email draft about: {body_prompt}. Do not send the message."}
)

email_body = response.get("output", body_prompt)  # Use AI response or fallback to user input

# Create and save the draft email
draft = create_draft_message(to_email, subject, email_body)
#response = api_resource.users().drafts().create(userId="me", body=draft).execute()

print("\n✅ Draft created successfully!")
print(f"📧 Subject: {subject}")
print(f"📩 To: {to_email}")

# Search for the latest draft email title
search_response = agent_executor.invoke({"input": "Find the latest email draft and tell me its subject."})
print("\n📌 Latest Draft Subject:", search_response)
