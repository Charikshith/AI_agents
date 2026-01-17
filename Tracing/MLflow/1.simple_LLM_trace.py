import mlflow
from openai import OpenAI

# Specify the tracking URI for the MLflow server.
mlflow.set_tracking_uri("http://localhost:5000")

# Specify the experiment you just created for your GenAI application.
mlflow.set_experiment("My Application1")

# Enable automatic tracing for all OpenAI API calls.
mlflow.openai.autolog()

client = OpenAI(base_url="http://192.168.29.193:4141/v1", api_key="Dummy_key")
# The trace of the following is sent to the MLflow server.
client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": "What's the weather like in Seattle?"},
    ],
)

