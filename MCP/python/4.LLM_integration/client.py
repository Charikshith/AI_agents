import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any , Dict, List, Optional
import logfire

import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI
import os
nest_asyncio.apply()

load_dotenv("D:\\Code\\ENVS\\.env")
logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))

class MCPLLMClient:
    """Client for interaction with LLM models using MCP tools"""

    def __init__(self,model:str ="deepseek-chat",base_url:str="https://api.deepseek.com/" ,api_key:str=None):
        """ Initialize the Client in OpenAI like style
            Args:
                model
                base_url
        """
        # Initialize session and client object
        self.session : Optional[ClientSession] = None
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None
        self.track: Optional[Any] = logfire.instrument_openai(self.client)
        self.exit_stack = AsyncExitStack()
    
    async def connect_to_server(self,server_script_path:str ="server.py"):
        """Connect to a MCP Server.
        Args:
            server_script_path: Path to the server script.
        """
        # Server Configuration
        server_params = StdioServerParameters(command='python', args=[server_script_path])
        
        # Connect to the server
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio , self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        # Initialize the connection
        await self.session.initialize()

        # List the tools available
        tools_result = await self.session.list_tools()
        print("\nConnected to server with tools:")
        for tool in tools_result.tools:
            print(f"- {tool.name} : {tool.description}")
        
    async def get_mcp_tools(self)->List[Dict[str,str]]:
        """Get available tools from the MCP server in OpenAI like style.
        Returns:
            List of tools.
        """
        tools_result = await self.session.list_tools()

        return [{
            "type": "function",
            "function": {
                "name":tool.name,
                "description":tool.description,
                "parameters":tool.inputSchema}
                }
                for tool in tools_result.tools
                ]
    
    async def process_query(self,query:str)->str:
        """Process a query using LLM and available MCP tools.
        
            Args:
                query: The user query.
            Returns:
                The response from the LLM
        """
        
        # Get the available tools
        tools = await self.get_mcp_tools()

        # Initial LLM API CALL

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": query
            }],
            tools=tools,
            tool_choice="auto"
        )

        # Get assistants response
        assistant_response = response.choices[0].message
        print(assistant_response)

        # Initialize conversation with the user query and assistant response
        messages = [
            {"role": "user", "content": query},
            assistant_response]
        
        # Handle tool calls if present

        if assistant_response.tool_calls:
            # Process each tool call
            for tool_call in assistant_response.tool_calls:
                # Execute the tool call
                result = await self.session.call_tool(
                    tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments)
                        )
                
                # Add tool response to conversation
                
                messages.append({
                    'role':'tool',
                    'tool_call_id':tool_call.id,
                    'content':result.content[0].text,
                })
            # Get the final response from the LLM with tool results
            final_response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="none"
            )
            return final_response.choices[0].message.content

        # NO tools calls just return the direct response
        return assistant_response.content
    
    async def cleanup(self):
        """Clean up ther resources"""
        await self.exit_stack.aclose()


async def main():
    """Main entry poin for the client"""

    client = MCPLLMClient(model=os.getenv("DEEPSEEKV3"),base_url=os.getenv("DEEPSEEK_URL") ,api_key=os.getenv("DEEPSEEK_API_KEY"))
    # client = MCPLLMClient(model='qwen2.5:32b',base_url=os.getenv("OLLAMA_URL") ,api_key=os.getenv("OLLAMA_API_KEY"))
    # logfire.instrument_openai(client)
    await client.connect_to_server("server.py")

    # Example: Ask about company vacation policy
    query = "What is our company's vacation policy?"
    print(f"\nQuery: {query}")

    response = await client.process_query(query)
    print(f"\nResponse: {response}")

    # Explicitly clean up resources before exiting main
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())








        
    
    
