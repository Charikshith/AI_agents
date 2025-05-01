import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()

async def main():
    # Define Server parameters
    server_params= StdioServerParameters(command="python",
                                         args=['server.py'],
                                         )
    
    # Connect to the server
    async with stdio_client(server=server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection:
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 2,"b": 7})
            print(result.content[0].text)

              
if __name__ == "__main__":
    
    asyncio.run(main())