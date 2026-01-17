# 🧠 Langfuse LLM Tracing Starter

This project demonstrates two simple ways to log and trace OpenAI-compatible Chat Completions API calls using [Langfuse](https://langfuse.com/).

---

## ✅ Requirements

- Python 3.8+
- [Langfuse SDK](https://docs.langfuse.com)
- OpenAI-compatible client (OpenAI, Azure OpenAI, or third-party proxy)

Install dependencies:

```bash
pip install langfuse openai
````

---

## 🔐 Environment Variables

Create a `.env` file or set these manually:

```env
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 📘 Step 4: Basic Logging Code Using Langfuse + OpenAI Client

### 🔹 Option 1: Manual Span Logging (Full Control)

```python
from langfuse import Langfuse
from openai import Client
import os, time

# Set env vars (optional if using .env)
os.environ["LANGFUSE_PUBLIC_KEY"] = "your_public_key"
os.environ["LANGFUSE_SECRET_KEY"] = "your_secret_key"
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

langfuse = Langfuse()

client = Client(api_key="sk-...", base_url="https://your-provider.com/v1")

def run_llm(prompt):
    trace = langfuse.trace(name="chat-completion", user_id="user-123")
    span = trace.span(name="openai-call")
    try:
        start = time.time()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        duration = time.time() - start
        output = response.choices[0].message.content
        span.end(output=output, metadata={"duration_sec": duration})
        return output
    except Exception as e:
        span.end(error_message=str(e))
        raise

print(run_llm("Explain Langfuse in one line."))
```

---

### 🔹 Option 2: Auto-Tracing with `langfuse.openai.OpenAI`

```python
from langfuse.openai import OpenAI
import os

os.environ["LANGFUSE_PUBLIC_KEY"] = "your_public_key"
os.environ["LANGFUSE_SECRET_KEY"] = "your_secret_key"
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

client = OpenAI(api_key="sk-...", base_url="https://your-provider.com/v1")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a haiku about Langfuse."}]
)

print(response.choices[0].message.content)
```

✅ This automatically traces:

* Prompt & response
* Model & latency
* Any errors or retries

---

## 📊 View Traces in Langfuse

Visit your project dashboard at:

```
https://cloud.langfuse.com
```

You’ll see:

* Trace names like `chat-completion` or `chat.completions.create`
* Metadata like duration, model, user ID, and more
* Full input/output inspection

---

## 🧪 Want More?

You can also:

* Add custom tool spans
* Track retry logic or failures
* Log nested agent chains

📘 Docs: [Langfuse Python SDK](https://docs.langfuse.com/sdk/python)



---

Let me know if you'd like this exported as a file (e.g. `README.md`) or included in a starter repo template.
```
