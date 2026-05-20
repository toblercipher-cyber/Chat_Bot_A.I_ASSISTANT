# AI Chatbot Assistant — Project Documentation

---

## Project Overview

This project is a fully functional AI Chatbot Assistant built using modern Large Language Model technologies. It connects to Mistral AI through the LangChain framework to enable intelligent, context-aware conversations directly in a web browser. The chatbot remembers the full conversation history, supports embedding-based document search, and is served through a professional web interface connected to a Python backend.

---

## What I Built

I built an AI-powered chatbot that:

- Accepts user questions through a web interface
- Sends those questions to a Python backend server
- Uses Mistral AI to generate intelligent, funny, and context-aware responses
- Remembers the full conversation history across all messages
- Can store and search through documents using embeddings
- Displays responses in a clean, professional UI with a 3D animated orb

---

## How It Works

**Step 1 — User types a message** in the browser chat interface.

**Step 2 — The frontend** sends that message to the Python backend running on port 8000.

**Step 3 — The backend** receives the message and appends it to the conversation history as a HumanMessage.

**Step 4 — LangChain** sends the full conversation history to the Mistral AI model.

**Step 5 — Mistral AI** generates a response based on the entire conversation context.

**Step 6 — The response** is sent back to the browser and displayed to the user.

**Step 7 — The response** is also saved into the conversation history as an AIMessage, so future replies remain context-aware.

---

## Conversation Memory

The chatbot uses three types of messages to maintain memory:

- **SystemMessage** — Sets the AI personality at the start. Example: "You are a funny AI agent"
- **HumanMessage** — Stores everything the user types
- **AIMessage** — Stores everything the bot replies

These three message types form a running list that grows with each exchange. The full list is sent to the model every time, which is why the bot remembers what was said earlier in the conversation.

---

## LangChain Implementation

**Chat Template** — LangChain provides ready-made message classes (SystemMessage, HumanMessage, AIMessage) that structure the conversation in the format Mistral AI expects. This is called the Chat Template pattern.

**Prompt Template** — For more advanced use cases, LangChain's ChatPromptTemplate allows creating reusable prompt structures with dynamic placeholders. For example, a placeholder called context can be filled with document content retrieved from the vector store, and question can be filled with the user's query.

**LCEL Pipeline** — LangChain Expression Language allows chaining all components together in one readable flow: retrieve documents → format context → build prompt → call model → parse output. This makes the code clean, modular, and easy to modify.

---

## Embeddings

**What are embeddings?**
Embeddings are numerical representations of text stored as vectors (lists of numbers). When two pieces of text have similar meaning, their vectors are mathematically close to each other. This allows searching for relevant content by meaning rather than by exact keywords.

**How I used embeddings:**
I used HuggingFace's sentence-transformers library to convert text into embeddings. The model used is all-MiniLM-L6-v2, which runs locally on CPU without requiring any API key.

**The process:**
1. Text documents are split into small chunks of around 500 tokens
2. Each chunk is converted into a 384-dimensional vector using the HuggingFace model
3. These vectors are stored in a vector database (ChromaDB or Qdrant)
4. When the user asks a question, the question is also embedded
5. The system finds the chunks most similar to the question
6. Those chunks are injected as context into the prompt before calling the AI model

This technique is called RAG (Retrieval-Augmented Generation) and allows the AI to answer questions about specific documents it was not originally trained on.

---

## HuggingFace Integration

HuggingFace was used in two ways in this project:

**Embeddings** — The sentence-transformers library from HuggingFace provides the all-MiniLM-L6-v2 model for converting text into vectors. This runs locally and is free.

**Model Access** — HuggingFace also provides access to hosted language models like DeepSeek-R1 through HuggingFaceEndpoint. This requires a free HuggingFace API token stored in the .env file as HUGGINGFACEHUB_API_TOKEN.

---

## API Keys Used

| Key | Service | Where Stored |
|---|---|---|
| MISTRAL_API_KEY | Mistral AI — main chatbot model | .env file |
| HUGGINGFACEHUB_API_TOKEN | HuggingFace — model access | .env file |
| GOOGLE_API_KEY | Google Gemini — optional model | .env file |

All API keys are stored in a .env file and loaded using python-dotenv. They are never written directly in the code.

---

## Project Folder Structure

```
MY__PROJECT__LLMS/
├── chatmodels/
│   ├── api.py              ← FastAPI backend server
│   ├── chatbot.py          ← Original terminal chatbot
│   └── chat.py             ← LangChain model experiments
├── embeddingmodels/
│   └── huggingface_embedding.py  ← Embedding experiments
├── .env                    ← API keys (private)
├── Requirements.txt        ← All Python dependencies
├── chatbot.html            ← Web UI frontend
└── .venv/                  ← Virtual environment
```

---

## Requirements

**Python Libraries:**

| Package | Purpose |
|---|---|
| langchain | Core LangChain framework |
| langchain-core | LCEL, prompts, message types |
| langchain-mistralai | Mistral AI integration |
| langchain-huggingface | HuggingFace embeddings |
| langchain-community | Community integrations |
| langchain-groq | Groq LLM access |
| langchain-openai | OpenAI integration |
| langgraph | Agent workflow graphs |
| fastapi | Python web API backend |
| uvicorn | ASGI server for FastAPI |
| pydantic | Request data validation |
| python-dotenv | Load .env API keys |
| sentence-transformers | Local embedding model |
| chromadb | Vector database |
| tiktoken | Token counting utility |
| torch | Deep learning backend |

**System Requirements:**
- Python 3.13 or higher
- Internet connection for API-based model calls
- 8GB RAM minimum

---

## Key Things I Learned

- Using response.content instead of the raw response object gives clean readable text output
- API keys must always go in a .env file, never hardcoded in source code
- Virtual environments isolate project packages and prevent version conflicts
- The SystemMessage + HumanMessage + AIMessage pattern is essential for conversation memory
- FastAPI requires CORS middleware enabled so browsers can make requests to it
- Embeddings allow searching by meaning, not just exact keywords
- faiss-cpu has no Python 3.13 support — use chromadb or qdrant instead
- The audioop module was removed in Python 3.13 — install audioop-lts for pydub support

---

## Running the Project

**Start the backend:**
```
python -m uvicorn chatmodels.api:app --reload --port 8000
```

**Open the UI:**
Double click chatbot.html in File Explorer — the chatbot opens in your browser ready to use.

---

*Built with LangChain + Mistral AI + HuggingFace + FastAPI*