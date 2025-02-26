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
    def __init__(self, file_path=None, question=""):
        # Determine agent type dynamically
        agent_type = "csv_agent" if file_path else "sql_agent"

        # ✅ Only pass `file` when `file_path` exists
        agent_params = {
            "agent_name": agent_type,
            "agent_type": agent_type
        }
        if file_path:  
            agent_params["file"] = File(csv_file=file_path)  # ✅ Only add file if present

        self.agent_runner = Agent(**agent_params)
        self.question = question

    def run(self):
        return self.agent_runner.run(self.question)

# Streamlit UI
st.title("Agent Runner")

# User must enter a question
question = st.text_input("Enter your question", "")

# File is optional
uploaded_file = st.file_uploader("Choose a CSV file (Optional)", type="csv")

# Save file to a temporary location if uploaded
temp_file_path = None
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name
    st.success(f"File uploaded and saved as: {temp_file_path}")

# Debugging
st.write(f"Debug: Question entered - '{question}'")
st.write(f"Debug: File path - '{temp_file_path}'")

# Ensure a question is provided
if question.strip():
    agent_runner_pipeline = AgentRunnerPipeline(file_path=temp_file_path, question=question)

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
else:
    st.warning("Please enter a question to proceed.")
