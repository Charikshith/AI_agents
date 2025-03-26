import os
from typing import List
from pocketflow import Node, Flow
from dotenv import load_dotenv
load_dotenv("D:\Code\AI\.env")

# --- (1) call_llm function ---
def call_llm(prompt: str, messages: List[dict] = None) -> str:
    """
    Calls the OpenAI GPT-4o model to generate a response based on the given prompt.

    Args:
        prompt: The prompt to send to the LLM.
        messages: Optional list of messages for chat history. If provided, the prompt will be appended as a user message.

    Returns:
        The LLM's response as a string.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
        Exception: If there is an error communicating with the OpenAI API.
    """
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        if messages:
            messages.append({"role": "user", "content": prompt})
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
        else:
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
        return r.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {e}")

# --- Summarization Node ---

class SummarizeNode(Node):
    def prep(self, shared):
        """Reads the text to summarize from the shared store."""
        return shared["text"]

    def exec(self, prep_res):
        """Calls the LLM to summarize the text."""
        prompt = f"Summarize the following text in approximately 50 words:\n\n{prep_res}"
        summary = call_llm(prompt)
        return summary

    def post(self, shared, prep_res, exec_res):
        """Writes the summary back to the shared store."""
        shared["summary"] = exec_res
        return "default"  # No specific action needed, just the default flow

# --- Test ---

if __name__ == "__main__":
    # Create the shared store
    shared = {}

    # Load data from file
    data_path = "./data/before.txt"
    if not os.path.exists("./data"):
        os.makedirs("./data")
    if not os.path.exists(data_path):
        with open(data_path, "w") as f:
            f.write("This is a sample text that will be summarized by the LLM. It contains a few sentences to demonstrate the summarization process. The goal is to condense this text into a shorter version, approximately 50 words in length, while retaining the core meaning and key information.")
    with open(data_path, "r") as f:
        shared["text"] = f.read()

    # Create the summarization node
    summarize_node = SummarizeNode()

    # Create a flow with the summarization node
    flow = Flow(start=summarize_node)

    # Run the flow
    flow.run(shared)

    # Print the summary from the shared store
    print("Original Text:\n", shared["text"])
    print("\nSummary:\n", shared["summary"])
