import os 
import sys
import time
import threading
import logfire
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.agents.csv_agent import CSVAgent



class File(BaseModel):
    csv_file : str = Field(..., title="CSV File Path", description="Path to the CSV file")
    
class question(BaseModel):
    questios : str = Field(..., title="Question", description="Question to be asked")
    
    
class Agent(BaseModel):
    agent_name: str = Field(..., title="Agent Name", description="Name of the agent")
    file: File = Field(..., title="File", description="File to be used by the agent")
    agent_type: str = Field(..., title="Agent Type", description="Type of the agent")
    
    
    def gate_check(self):
        if self.agent_type == 'csv_agent':
            return True
    
    def create_agent(self):
        if self.agent_type == 'csv_agent':
            return CSVAgent(file_path=self.file.csv_file)
        else:
            raise ValueError('Agent type not found')
        
    def run(self, question: str):  
        agent = self.create_agent()
        response = agent.run_agent(question=question)  # Capture the response
        return response  # ✅ Return the responsey
        