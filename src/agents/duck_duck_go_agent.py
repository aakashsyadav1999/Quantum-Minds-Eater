from langchain_community.tools import DuckDuckGoSearchRun


class DuckDuckGoAgent:
    
    def __init__(self):
        self.search = DuckDuckGoSearchRun(max_results=1)
        
    def run(self, query):
        print("DuckDuckGoAgent: Running query: ", query)
        return self.search.run(query)
    
    

duck_duck_go_agent = DuckDuckGoAgent()
#duck_duck_go_agent.run("What is the capital of France?")
print(duck_duck_go_agent.run("What is the capital of France?"))