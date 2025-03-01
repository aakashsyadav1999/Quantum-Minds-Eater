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
# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")        
class Email:
    
    # Initialize Email class
    def __init__(self, to_email, subject, body):
        self.to_email = to_email
        self.subject = subject
        self.body = body
        
    # Load Gmail credentials   
    def credentials(self):
        # Load Gmail credentials
        return get_gmail_credentials(
            token_file="token.json",
            scopes=["https://www.googleapis.com/auth/gmail.compose"],
            client_secrets_file="credentials.json",
        )

    # Build Gmail API resource
    def build_resource_service(self, credentials):
        # Build Gmail API resource
        api_resource = build_resource_service(credentials=credentials)
        return api_resource
    
    # Initialize Gmail Toolkit
    def toolkit(self, api_resource):
        # Initialize Gmail Toolkit
        toolkit = GmailToolkit(api_resource=api_resource)
        GmailToolkit.model_rebuild()  # Fix for Pydantic model issue
        
        return toolkit
    
    # Setup LangChain Agent
    def langchain_agent(self):
        # Setup LangChain Agent
        instructions = "You are an assistant."
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)
        llm = ChatOpenAI(temperature=0)
        
        return llm, prompt
    
    # Create Agent
    def agent_executor_function(self, llm, toolkit, prompt):
        # Create Agent
        agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=toolkit.get_tools(),
            verbose=False,  # Prevents email content from being displayed
        )
        
        return agent_executor

    # Function to create a valid email draft
    def create_draft_message(self, to_email, subject, body):
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
    def get_user_input(self,agent_executor):
        # Get user input
        to_email = self.to_email
        subject = self.subject
        body_prompt = self.body
                
        # Generate AI content for the email
        agent_executor.invoke(
            {"input": f"Write a professional email draft about: {body_prompt}. Do not send the message."}
        )
        
        print("\n✅ Draft created successfully!")
        print(f"📧 Subject: {subject}")
        print(f"📩 To: {to_email}")

        # Search for the latest draft email title
        search_response = agent_executor.invoke({"input": "Find the latest email draft and tell me its subject."})
        print("\n📌 Latest Draft Subject:", search_response)
    
    # Run the Email class 
    def run(self):
        # Load Gmail credentials
        credentials = self.credentials()
        # Build Gmail API resource
        api_resource = self.build_resource_service(credentials)
        # Initialize Gmail Toolkit
        toolkit = self.toolkit(api_resource)
        # Setup LangChain Agent
        llm, prompt = self.langchain_agent()
        # Create Agent
        agent_executor = self.agent_executor_function(llm, toolkit, prompt)
        # Get user input
        self.get_user_input(agent_executor)
    
# Initialize Email class
if __name__ == "__main__":
    email = Email(to_email=input("Enter recipient's email: ").strip(),
                  subject=input("Enter email subject: ").strip(),
                  body=input("Enter a short description of your email content: ").strip())
    email.run()
