import os 
import sys
import logfire
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.agents.csv_agent import CSVAgent
from src.agents.sql_agent import MSSQL
from src.agents.email_agent import Email

class File(BaseModel):
    csv_file: str = Field(..., title="CSV File Path", description="Path to the CSV file")

class Question(BaseModel):  # ✅ Corrected class name (uppercase for class names)
    question: str = Field(..., title="Question", description="Question to be asked")

class Agent(BaseModel):
    agent_name: str
    agent_type: str
    file: Optional[File] = None
    question: Optional[str] = None
    detected_agent_type: Optional[str] = None
    to_email: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    agent: Optional[object] = None  # ✅ Define `agent` here

    def __init__(self, **data):
        super().__init__(**data)

        self.detected_agent_type = self.gate_check()
        self.to_email = data.get("to_email", None)
        self.subject = data.get("subject", None)
        self.body = data.get("body", None)
        
        # ✅ Now, assign `self.agent` after initialization
        self.agent = self._initialize_agent()

    def gate_check(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = f"Given the agent type '{self.agent_type}', should the agent use a CSV file or an SQL database? or else should it send an email?"
        response = llm.invoke(prompt)
        response_text = response.content if hasattr(response, "content") else str(response)

        print(f"LLM Response: {response_text}")  # ✅ Debugging

        if 'csv_agent' in response_text:
            return 'csv_agent'
        elif 'sql_agent' in response_text:
            return 'sql_agent'
        elif 'email' in response_text:
            return 'email_agent'
        else:
            raise ValueError('Unable to determine the agent type')

    def _initialize_agent(self):
        if self.detected_agent_type == "csv_agent":
            if not self.file or not self.file.csv_file:
                raise ValueError("CSV file is required but not provided.")
            return CSVAgent(file_path=self.file.csv_file)
        elif self.detected_agent_type == "sql_agent":
            if not self.question:
                raise ValueError("SQL agent requires a question.")
            return MSSQL()
        elif self.detected_agent_type == "email_agent":
            if not self.to_email or not self.subject or not self.body:
                raise ValueError("Missing email parameters: to_email, subject, or body.")
            return Email(to_email=self.to_email, subject=self.subject, body=self.body)
        else:
            raise ValueError("Invalid agent type")

    def run(self, question: Optional[str] = None):
        if self.detected_agent_type in ["csv_agent", "sql_agent"]:
            if not question:
                raise ValueError("A question is required for CSV/SQL agents.")
            return self.agent.run_agent(question=question)  # ✅ Pass question for CSV/SQL

        elif self.detected_agent_type == "email_agent":
            return self.agent.run_agent()  # ✅ Do NOT pass `question`
