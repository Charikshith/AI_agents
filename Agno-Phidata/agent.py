# Welcome to the Agno Cookbook

#-------------------------------------------------------
# 1. Simple Agent to chat ( Open AI like )
#-------------------------------------------------------

from dotenv import load_dotenv
load_dotenv("D:\\Code\\AI\\.env")
# Make sure your api key are present and with same variable name

from os import getenv
from agno.agent import Agent, RunResponse
from agno.models.openai.like import OpenAILike

agent = Agent(
    model=OpenAILike(
        id="deepseek-chat",
        api_key=getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/",
    )
)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")


#-------------------------------------------------------
# 1. Simple Agent to chat ( Direct Import)
#-------------------------------------------------------

from agno.agent import Agent, RunResponse
from agno.models.deepseek import DeepSeek

agent = Agent(model=DeepSeek(), markdown=True)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")




from agno.agent import Agent
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.openai.like import OpenAILike
from os import getenv

from agno.utils.pprint import pprint_run_response
agent = Agent( model=OpenAILike(
        id="deepseek-chat",
        api_key=getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/",
    ),
    description=""" You are a famous short story writer asked to write for a magazine.""",
    instructions=["You are a pilot on a plane flying from Hawaii to Japan."],
    markdown=True,
    debug_mode=True,
    )


# Run agent and return the response as a stream
response_stream: Iterator[RunResponse] =agent.run("Tell me a 5 sentence horror story.",stream=True)

# Print the response stream in markdown format
pprint_run_response(response_stream, markdown=True)