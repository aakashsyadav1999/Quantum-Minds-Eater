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

        if agent_type in ["csv_agent", "sql_agent"]:
            if not question:  # Ensure question is not None
                raise ValueError("Question is required for CSV/SQL agents.")
            agent_params["question"] = question  # ✅ Only for CSV/SQL agents

        if agent_type == "csv_agent" and file_path:
            agent_params["file"] = File(csv_file=file_path)

        if agent_type == "email_agent":
            if not all([to_email, subject, body]):
                raise ValueError("Email agent requires recipient's email, subject, and body.")
            agent_params.update({"to_email": to_email, "subject": subject, "body": body})

        self.agent_runner = Agent(**agent_params)

    def run(self):
        return self.agent_runner.run()

# Streamlit UI
st.title("Agent Runner")

# Select Agent Type
agent_type = st.selectbox("Select an Agent Type", ["csv_agent", "sql_agent", "email_agent"])

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
if agent_type in ["csv_agent", "sql_agent"]:
    question = st.text_input("Enter your question", "")

# Email Inputs (Only for Email Agent)
to_email, subject, body = None, None, None
if agent_type == "email_agent":
    to_email = st.text_input("Enter recipient's email", "")
    subject = st.text_input("Enter email subject", "")
    body = st.text_area("Enter email content", "")

# Debugging
st.write(f"Debug: Agent Type - '{agent_type}'")
if question:
    st.write(f"Debug: Question entered - '{question}'")
if temp_file_path:
    st.write(f"Debug: File path - '{temp_file_path}'")

# Ensure the required inputs are provided
if (agent_type in ["csv_agent", "sql_agent"] and not question.strip()):
    st.warning("Please enter a question to proceed.")
elif (agent_type == "email_agent" and not all([to_email, subject, body])):
    st.warning("Please fill in all email fields to proceed.")
else:
    agent_runner_pipeline = AgentRunnerPipeline(
        agent_type=agent_type,
        file_path=temp_file_path,
        question=question,
        to_email=to_email,
        subject=subject,
        body=body
    )

    # Run agent on button click
    if st.button("Run Agent"):
        with st.spinner("Running agent... Please wait ⏳"):
            try:
                response = agent_runner_pipeline.run()
                st.success("Agent has finished running ✅")
                st.write("### Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error while running agent: {str(e)}")
