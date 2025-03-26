import os
from openai import OpenAI
from typing import List
from dotenv import load_dotenv
load_dotenv("D:\\Code\\AI\\.env")

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

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        if messages:
            messages.append({"role": "user", "content": prompt})
            r = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
        else:
            r = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
        return r.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {e}")


# --- (2) get_embedding function ---

def get_embedding(text: str) -> List[float]:
    """
    Gets the embedding for the given text using the OpenAI text-embedding-ada-002 model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
        Exception: If there is an error communicating with the OpenAI API.
    """

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        resp = client.embeddings.create(model="text-embedding-ada-002", input=text)
        return resp.data[0].embedding
    except Exception as e:
        raise Exception(f"Error getting embedding from OpenAI API: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # Set the API key as an environment variable (for security)
    # In your terminal, run: export OPENAI_API_KEY="your_actual_api_key"
    # Or set it in your IDE's environment variables

    try:
        # Example usage of call_llm
        response = call_llm("How are you?")
        print(f"LLM Response: {response}")

        # Example usage of call_llm with chat history
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
        ]
        response = call_llm("What is the capital of Germany?", messages)
        print(f"LLM Response with chat history: {response}")

        # Example usage of get_embedding
        embedding = get_embedding("Hello, world!")
        print(f"Embedding: {embedding[:10]}... (truncated to first 10 elements)")  # Print only the first 10 elements for brevity

    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the OPENAI_API_KEY environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
