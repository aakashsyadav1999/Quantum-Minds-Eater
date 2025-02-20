from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os
allow_dangerous_code=True

load_dotenv(find_dotenv())

class CSVAgent:
    
    def __init__(self,file_path):
        self.file = file_path
    
    def get_agent(self):
        agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY")),
        self.file,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code = True
        )   
        return agent
    
    def run_agent(self, question):
        response = self.get_agent().run(question)
        print(response)
        return response
            