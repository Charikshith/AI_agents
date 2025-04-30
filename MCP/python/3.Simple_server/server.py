from mcp.server.fastmcp import FastMCP


# Create an MCP Server
mcp = FastMCP(  name="Calculator",
                host="127.0.0.1",  # only used for SSE transport (localhost)
                port=8050,  # only used for SSE transport (set this to any port)
            )

# ADD 
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# RUN the server
if __name__ == "__main__":
    transport = "sse"
    if transport =='stdio':
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == 'sse':
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")