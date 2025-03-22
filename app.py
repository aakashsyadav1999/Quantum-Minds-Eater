import os
import sys
import tempfile
import streamlit as st

# Ensure correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import necessary components
from src.components.agent_runner import Agent, File

# Define AgentRunnerPipeline
class AgentRunnerPipeline:
    def __init__(self, agent_type, file_path=None, question=None, to_email=None, subject=None, body=None):
        # Prepare agent parameters dynamically
        agent_params = {"agent_name": agent_type, "agent_type": agent_type}

        # Ensure question is valid for SQL/CSV agents
        if agent_type in ["csv_agent", "sql_agent"]:
            if not question or not question.strip():  # Fix: Strip whitespace and validate
                raise ValueError("Question is required for CSV/SQL agents.")
            agent_params["question"] = question.strip()  # Fix: Pass stripped question

        if agent_type == "csv_agent" and file_path:
            agent_params["file"] = File(csv_file=file_path)

        if agent_type == "email_agent":
            if not all([to_email, subject, body]):
                raise ValueError("Email agent requires recipient's email, subject, and body.")
            agent_params.update({"to_email": to_email, "subject": subject, "body": body})
            
        if agent_type in ["website_research"]:
            if not question or not question.strip():  # Fix: Strip whitespace and validate
                raise ValueError("Question is required for website_research agents.")
            agent_params["question"] = question.strip()  # Fix: Pass stripped question

        # Debugging - Ensure agent parameters are correct
        st.write(f"Debug: Agent parameters - {agent_params}")

        self.agent_runner = Agent(**agent_params)

    def run(self):
        return self.agent_runner.run()

# Streamlit UI
st.title("Agent Runner")

# Select Agent Type
agent_type = st.selectbox("Select an Agent Type", ["csv_agent", "sql_agent", "email_agent", "website_research"])

# CSV File Upload (Only for CSV Agent)
temp_file_path = None
if agent_type == "csv_agent":
    uploaded_file = st.file_uploader("Choose a CSV file (Optional)", type="csv")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name
        st.success(f"File uploaded and saved as: {temp_file_path}")

# Inputs for CSV/SQL Agents
question = None
if agent_type in ["csv_agent", "sql_agent", "website_research"]:
    question = st.text_input("Enter your question", "").strip()  # Fix: Strip whitespace

# Email Inputs (Only for Email Agent)
to_email, subject, body = None, None, None
if agent_type == "email_agent":
    to_email = st.text_input("Enter recipient's email", "")
    subject = st.text_input("Enter email subject", "")
    body = st.text_area("Enter email content", "")

# Debugging - Log user inputs
st.write(f"Debug: Agent Type - '{agent_type}'")
st.write(f"Debug: Captured question before processing: '{question}' (Type: {type(question)})")
if temp_file_path:
    st.write(f"Debug: File path - '{temp_file_path}'")

# Validation checks before running the agent
can_proceed = True

if agent_type in ["csv_agent", "sql_agent"] and not question:
    st.warning("Please enter a question to proceed.")
    can_proceed = False
elif agent_type == "email_agent" and not all([to_email, subject, body]):
    st.warning("Please fill in all email fields to proceed.")
    can_proceed = False
elif agent_type in ["website_research"] and not question:
    st.warning("Please enter a question to proceed.")
    can_proceed = False

# Run agent on button click only if validation passes
if st.button("Run Agent") and can_proceed:
    with st.spinner("Running agent... Please wait ⏳"):
        try:
            # Debugging before execution
            st.write(f"Debug - Final question value being passed: '{question}' (type: {type(question)})")
            
            agent_runner_pipeline = AgentRunnerPipeline(
                agent_type=agent_type,
                file_path=temp_file_path,
                question=question,
                to_email=to_email,
                subject=subject,
                body=body
            )
            response = agent_runner_pipeline.run()
            st.success("Agent has finished running ✅")
            st.write("### Response:")
            st.write(response)
        except Exception as e:
            st.error(f"Error while running agent: {str(e)}")