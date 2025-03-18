from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.tavily import TavilyTools
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import os
load_dotenv()

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=Ollama(id="llama3.2:latest"),
    tools=[TavilyTools(api_key=os.getenv('TAVILY_API_KEY'))],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Ollama(id="llama3.2:latest"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Summarize analyst recommendations and share the latest news for Nvidia", stream=True)
