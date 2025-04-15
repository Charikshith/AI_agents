# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()
deepseek_client = AsyncOpenAI( api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/",)
deepseek=OpenAIChatCompletionsModel( model="deepseek-chat", openai_client=deepseek_client, )


# FastAPI app
app = FastAPI(title="OpenAI SDK Chat API")

# Supported OpenAI models
MODEL_NAMES = ["deepseek-chat", "gpt-4"]

# Request schema
class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]  # Alternating user-assistant messages, starting with user

# POST /chat endpoint
@app.post("/chat")
async def chat_endpoint(request: RequestState):
    print("REQUEST:",request)
    if request.model_name not in MODEL_NAMES:
        return {"error": "Invalid model name. Use one of: " + ", ".join(MODEL_NAMES)}

    # Merge message history into a single prompt (simplified)
    combined_prompt = "\n".join(request.messages)

    # Create and run agent
    agent = Agent(name="Assistant", instructions=request.system_prompt, model=OpenAIChatCompletionsModel( model=request.model_name, openai_client=deepseek_client, ))
    result = await Runner.run(agent, combined_prompt)
    print("RESULT:",result.final_output)
    return {"response": result.final_output}

# Run with: uvicorn main:app --reload
