import os
import json
from mcp.server.fastmcp import FastMCP

# Create a MCP server
mcp = FastMCP(name="Knowledge_Base",
              host="127.0.0.1",
              port=8050)

@mcp.tool()
def get_knowledge_base() -> str:
    """ Retrive the entire knowledge base as a formatted string.
        Returns:
            A formatted string containing all Q&A pairs from the knowledge base.
    """
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "data","kb.json")
        with open(kb_path, "r") as f:
            kb = json.load(f)
        
        # Format the knowledge base as a string
        kb_text = "Here is the retrived knowledge base:\n\n"
        
        if isinstance(kb,dict):
            for i,item in enumerate(kb,1):
                if isinstance(item,dict):
                        
                    question = item.get("question","Unkown")
                    answer = item.get("answer","Unkown")
                else:
                    question = f"item {i}"
                    answer = str(item)
        else:
            kb_text += f"Knowledge base content: {json.dumps(kb,indent=2)}"
        return kb_text

    except FileNotFoundError:
        return "Knowledge base not found."
    except json.JSONDecodeError:
        return "Error decoding JSON data."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    # Run the server
if __name__ == "__main__":
    mcp.run(transport='stdio')
    

            