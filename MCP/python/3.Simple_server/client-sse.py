import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()
"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8050.

To run the server:
python server.py
"""
async def main():
    # Connect to the server using SSE
    async with sse_client("http://127.0.0.1:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            # Initialize the connection 
            await session.initialize()

            # List the tools available
            tools_result = await session.list_tools()
            print("Tools available:")
            for tool in tools_result.tools:
                print(f"- {tool.name} : {tool.description}")

            # Cal out calculator tool
            result = await session.call_tool("add", arguments={"a": 1, "b": 3})
            print(f" Result is {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())