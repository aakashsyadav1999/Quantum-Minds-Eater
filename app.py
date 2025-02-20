#Streamlit app
import os
import sys
import threading
import tempfile
import streamlit as st

# Ensure correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import necessary components
from src.components.agent_runner import Agent, File

# Define AgentRunnerPipeline
class AgentRunnerPipeline:
    def __init__(self, file_path, question):
        self.agent_runner = Agent(
            agent_name="CSV Agent",
            file=File(csv_file=file_path),  # ✅ Correctly initializing File
            agent_type="csv_agent"
        )
        self.question = question  # Store question separately

    def run(self):
        return self.agent_runner.run(self.question)  # ✅ Correctly passing question

# Streamlit UI
st.title("CSV Agent Runner")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Save file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name  # Get temporary file path

    st.success(f"File uploaded and saved as: {temp_file_path}")

    # Add user input for the question
    question = st.text_input("Enter your question", "How many rows are in the CSV?")

    # Initialize agent
    agent_runner_pipeline = AgentRunnerPipeline(file_path=temp_file_path, question=question)

    # Function to run agent in a separate thread
    def run_agent():
        try:
            agent_runner_pipeline.run()
            st.success("Agent has finished running ✅")
        except Exception as e:
            st.error(f"Error while running agent: {str(e)}")

    # Run agent on button click
    if st.button("Run Agent"):
        with st.spinner("Running agent... Please wait ⏳"):
            try:
                response = agent_runner_pipeline.run()  # ✅ Capture response
                st.success("Agent has finished running ✅")
                st.write("### Response:")
                st.write(response)  # ✅ Display response in UI
            except Exception as e:
                st.error(f"Error while running agent: {str(e)}")