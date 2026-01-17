Got it ✅ — here’s a **structured problem statement** you can send to the LangChain/LangGraph team. It summarizes all the issues you ran into and why you had to design your own state.

---

# 📌 Problem Statement: Incompatibility Between `MessagesState` and OpenAI Chat Completions API in LangGraph

Hello LangChain Team,

I’ve been building agent workflows with **LangGraph** + **OpenAI Chat Completions API**, and I’ve consistently run into problems when using the provided `MessagesState`. After a long debugging cycle, here’s a detailed description of the issue and why it matters.

---

## 🔎 Background

* **LangGraph encourages using `MessagesState`** for chat-style agents.
* `MessagesState` internally stores messages as **LangChain `BaseMessage` objects** (`HumanMessage`, `AIMessage`, `SystemMessage`, `ToolMessage`).
* However, the **OpenAI `chat.completions.create` API** expects messages as a list of **plain dicts** in the form:

  ```python
  {"role": "user"|"assistant"|"system"|"tool", "content": "...", ...}
  ```

---

## ❌ The Problem

When I connect LangGraph → OpenAI, I keep getting errors such as:

```
AttributeError: 'AIMessage' object has no attribute 'get'
```

or

```
BadRequestError: Request contains an invalid argument
```

Root cause: `state["messages"]` contains **LangChain message objects** instead of dicts.

Examples:

* A `HumanMessage` looks like:

  ```python
  HumanMessage(content="Hello", additional_kwargs={}, response_metadata={})
  ```

  but the API requires:

  ```python
  {"role": "user", "content": "Hello"}
  ```

* A `ToolMessage` in LangChain:

  ```python
  ToolMessage(content="42", tool_call_id="call_123")
  ```

  vs OpenAI requirement:

  ```python
  {"role": "tool", "tool_call_id": "call_123", "content": "42"}
  ```

* `AIMessage` with tool calls stores them in attributes/kwargs, but OpenAI requires:

  ```python
  {
    "role": "assistant",
    "content": "",
    "tool_calls": [
      {"id": "...", "type": "function", "function": {"name": "...", "arguments": "..."}}
    ]
  }
  ```

This mismatch forces me to write a custom `lc_to_openai()` converter or replace `MessagesState` entirely.

---

## ⚙️ Current Workaround

To avoid repeated conversion, I had to:

1. Create a **custom graph state**:

   ```python
   class ChatState(TypedDict):
       messages: Annotated[List[Dict[str, Any]], append_messages]
   ```

   where messages are stored **only in OpenAI dict format**.

2. Replace LangGraph’s default `add_messages` reducer with a custom `append_messages` reducer that never creates LangChain objects.

3. Strip unsupported fields (`name` on tool messages, etc.) to comply with OpenAI’s schema.

This works, but it means I **cannot use `MessagesState` at all**, even though it’s presented as the recommended pattern.

---

## ❓ Questions for the LangChain Team

1. **Is `MessagesState` intended to work directly with OpenAI `chat.completions` API?**
   Right now, it doesn’t, because it yields `HumanMessage/AIMessage` objects instead of dicts.

2. **Should LangGraph provide an OpenAI-compatible state out of the box?**
   For example, something like `OpenAIMessageState` that stores `{"role": ..., "content": ...}` dicts instead of LangChain objects.

3. **Is there an official utility to convert `MessagesState` into OpenAI message dicts?**
   I had to roll my own `lc_to_openai()` converter, but I suspect many users will hit the same issue.

4. **Tool message schema alignment:**
   Why does `ToolMessage` include a `name` field, while OpenAI rejects it in `role="tool"` messages? Should this be normalized internally?

---

## 📌 Impact

* Increases boilerplate and confusion: developers expect `MessagesState` to be plug-and-play with OpenAI.
* Leads to subtle bugs (`.get` on `AIMessage`, bad request 400s).
* Forces developers to either:

  * abandon `MessagesState`, or
  * constantly normalize/convert messages at every node.

---

## ✅ Suggested Improvements

* Provide a **first-class OpenAI-compatible state** (dict-based, not `BaseMessage`-based).
* Add a built-in utility: `to_openai_messages(state["messages"])`.
* Document clearly when `MessagesState` is useful (LangChain-native pipelines) vs when OpenAI dicts are required.
* Align `ToolMessage` schema with OpenAI’s spec (no extra `name` field for tool responses).

---

👉 In short: **LangGraph’s `MessagesState` and OpenAI Chat Completions API don’t interoperate cleanly.** I’d love guidance on whether this is by design, or if future versions will provide OpenAI-dict compatible state handling.

Thanks!
*(Your Name)*

---

Do you want me to also include a **minimal reproducible example (MRE)** showing the error (`AIMessage has no attribute 'get'`) so the LangChain team can run it and see the failure directly?
