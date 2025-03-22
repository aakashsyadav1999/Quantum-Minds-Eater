from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

class WebsiteResearchAgent:
    def __init__(self, question):
        self.question = question

    def website_research_agent(self):
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[DuckDuckGo()],
            description="You are a senior NYT researcher writing an article on a topic.",
            instructions=[
                "For a given topic, search for the top 5 links.",
                "Then read each URL and extract the article text. If a URL isn't available, ignore it.",
                "Analyze and prepare an NYT-worthy article based on the information.",
            ],
            markdown=False,
            show_tool_calls=True,
            add_datetime_to_instructions=True,
        )
        return agent

    def run_agent(self):  #  Corrected method
        agent_instance = self.website_research_agent()
        return agent_instance.run(self.question)  #  Corrected method to run the agent
