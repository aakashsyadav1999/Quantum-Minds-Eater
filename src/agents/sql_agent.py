from langchain_community.utilities.sql_database import SQLDatabase
import pyodbc

# Updated connection string with additional parameters for troubleshooting
db = SQLDatabase.from_uri("mssql+pyodbc://ray:advicr49--@192.168.29.221,2021/health?driver=ODBC+Driver+17+for+SQL+Server&timeout=30&TrustServerCertificate=yes")

from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

agent_executor.invoke(
    "What is the average BMI of the patients?",
)