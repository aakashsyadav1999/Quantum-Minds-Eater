from langchain_community.utilities.sql_database import SQLDatabase
import pyodbc
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

# Updated connection string with additional parameters for troubleshooting
db = SQLDatabase.from_uri("mssql+pyodbc://ray:advicr49--@192.168.29.221,2021/health?driver=ODBC+Driver+17+for+SQL+Server&timeout=30&TrustServerCertificate=yes")


class MSSQL:
    
    def __init__(self):
        self.db = db
        
    def call_sql_agent(self, query):
        return self.db.execute(query)
    
    def get_sql_agent(self):
        return self.db
    
    def get_sql_agent_executor(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        agent_executor = create_sql_agent(llm, db=self.db, agent_type="openai-tools", verbose=True)  
        return agent_executor
    
    def run_agent(self, question):
        response = self.get_sql_agent_executor().run(question)
        return response   
    
    

if __name__ == '__main__':
    agent = MSSQL(db)
    agent.run_agent(question=input("Enter your question: "))






