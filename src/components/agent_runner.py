import os 
import sys
import logfire
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.agents.csv_agent import CSVAgent
from src.agents.sql_agent import MSSQL

class File(BaseModel):
    csv_file: str = Field(..., title="CSV File Path", description="Path to the CSV file")

class Question(BaseModel):  # ✅ Corrected class name (uppercase for class names)
    question: str = Field(..., title="Question", description="Question to be asked")

class Agent(BaseModel):
    agent_name: str = Field(..., title="Agent Name", description="Name of the agent")
    agent_type: str = Field(..., title="Agent Type", description="Type of the agent")
    file: Optional[File] = Field(None, title="File", description="File to be used by the agent")

    class Config:  
        extra = "allow"

    def __init__(self, **data):
        super().__init__(**data)
        self.detected_agent_type = self.gate_check()  # ✅ Store agent type only once

    def gate_check(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = f"Given the agent type '{self.agent_type}', should the agent use a CSV file or an SQL database?"
        response = llm.invoke(prompt)
        response_text = response.content if hasattr(response, "content") else str(response)

        print(f"LLM Response: {response_text}")  # ✅ Debugging

        if 'csv_agent' in response_text:
            return 'csv_agent'
        elif 'sql_agent' in response_text:
            return 'sql_agent'
        else:
            raise ValueError('Unable to determine the agent type')

    def csv_agent(self):
        if self.detected_agent_type == 'csv_agent':  # ✅ Corrected method usage
            if not self.file or not self.file.csv_file:
                raise ValueError("CSV file is required for CSV agent but not provided.")
            return CSVAgent(file_path=self.file.csv_file)
        raise ValueError('Agent type not found')

    def mssql_agent(self):
        if self.detected_agent_type == 'sql_agent':  # ✅ Corrected method usage
            return MSSQL()
        raise ValueError('Agent type not found')

    def run(self, question: str):
        print(f"Final Agent Type: {self.detected_agent_type}")  # ✅ Debugging
        if self.detected_agent_type == 'csv_agent':
            agent = self.csv_agent()
        elif self.detected_agent_type == 'sql_agent':
            agent = self.mssql_agent()
        else:
            raise ValueError('Agent type not found')

        return agent.run_agent(question=question)
