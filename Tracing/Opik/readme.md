# 🔍 OpenAI-Compatible LLM Tracing with Opik

This guide shows how to trace OpenAI-compatible LLM calls using **[Opik](https://github.com/langroid/opik)** — a lightweight and local-first observability and debugging tool for prompt-based workflows.

---

## ✅ Features of Opik

- Trace LLM calls and responses
- Visualize prompts and outputs in a browser UI
- Works with OpenAI and compatible APIs
- Local storage of traces (no external dashboard required)

---

## ✅ Requirements

```bash
pip install opik openai
````

---

## 🛠️ Step-by-Step Setup

### 🔹 1. Initialize Opik and OpenAI Client

```python
from opik import trace, show
from openai import Client

client = Client(api_key="sk-...", base_url="https://your-provider.com/v1")
```

---

### 🔹 2. Trace an OpenAI-Compatible LLM Call

```python
@trace(name="basic-chat-completion")
def run_chat():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Explain observability in one line."}
        ]
    )
    return response.choices[0].message.content

print(run_chat())
```

---

### 🔹 3. Visualize Your Traces

After running your script, open your browser:

```bash
opik view
```

This will launch a local web UI (usually at [http://127.0.0.1:8000](http://127.0.0.1:8000)) where you can:

* View each call’s input/output
* See prompt history
* Compare responses

---

## 💡 Why Use Opik?

| Feature           | Benefit                        |
| ----------------- | ------------------------------ |
| Local-first       | No cloud, no credentials       |
| OpenAI-compatible | Works with any provider        |
| Interactive UI    | Browse and debug easily        |
| Fast setup        | Just a decorator + `opik view` |

---

## 🧪 Advanced Usage

You can also:

* Trace tool calls
* Annotate spans and metadata
* Use in LangGraph or agent-based systems

📘 More: [Opik GitHub Repo](https://github.com/langroid/opik)

---

Let me know if you'd like a bundled version with `.py` starter files or both Langfuse and Opik integrated in one repo.
```
