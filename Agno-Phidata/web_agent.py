from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os
load_dotenv()

web_agent = Agent(
    name="Web Agent",
    model=Ollama(id="llama3.2:latest"),
    tools=[TavilyTools(api_key=os.getenv('TAVILY_API_KEY'))],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)
web_agent.print_response("Whats happening allu ajun sudharshan theatre accident?", stream=True)
