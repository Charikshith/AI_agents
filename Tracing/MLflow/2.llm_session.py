import mlflow
from openai import OpenAI
# Specify the tracking URI for the MLflow server.

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("My Application1")
mlflow.openai.autolog()
client = OpenAI(base_url="http://192.168.29.193:4141/v1", api_key="Dummy_key")

@mlflow.trace
def chat_completion(message: str, user_id: str, session_id: str):
    # Set these metadata keys to associate the trace to a user and session
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user": user_id,
            "mlflow.trace.session": session_id,
        }
    )

    # Invoke the OpenAI chat completion API with the provided message
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
    )
    return response

if __name__ == "__main__":
    # Depending on your setup, user and session IDs can be passed to your
    # server handler via the network request from your client applications,
    # or derived from some other request context.
    user_id = "user-123"
    session_id = "session-123"

    chat_completion("Hello, how are you?", user_id, session_id)
    print(chat_completion("Hello, how are you?", user_id, session_id))
