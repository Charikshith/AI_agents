import streamlit as st
import requests

# Streamlit App Configuration
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")

# Define API endpoint
API_URL = "http://127.0.0.1:8000/chat"

# Predefined models
# Supported OpenAI models
MODEL_NAMES = ["deepseek-chat", "gpt-4"]
# Streamlit UI Elements
st.title("LangGraph Chatbot Agent")
st.write("Interact with the LangGraph-based agent using this interface.")

# Input box for system prompt
given_system_prompt = st.text_area("Define you AI Agent:", height=100, placeholder="Type your system prompt here...")
# # Option 1: Use default height
# given_system_prompt = st.text_area("Define your AI Agent:", placeholder="Type your system prompt here...")

# # Option 2: Set height to the minimum allowed (or more)
# given_system_prompt = st.text_area("Define your AI Agent:", height=100, placeholder="Type your system prompt here...")


# Dropdown for selecting the model
selected_model = st.selectbox("Select Model:", MODEL_NAMES)

# Input box for user messages
user_input = st.text_area("Enter your message(s):", height=150, placeholder="Type your message here...")

# Button to send the query
if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            try:
                # Send the input to the FastAPI backend
                payload = {
                    "messages": [user_input],
                    "model_name": selected_model,
                    'system_prompt': given_system_prompt
                }
                response = requests.post(API_URL, json=payload)

                # Display the response
                if response.status_code == 200:
                    response_data = response.json()
                    if "error" in response_data:
                        st.error(response_data["error"])
                    elif "response" in response_data:
                        st.subheader("Agent Response:")
                        st.markdown(f"**Final Response:** {response_data['response']}")
                    else:
                        st.warning("No response field found in the agent output.")

                else:
                    st.error(f"Request failed with status code {response.status_code}.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message before clicking 'Send Query'.")