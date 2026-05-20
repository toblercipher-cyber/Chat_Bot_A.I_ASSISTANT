# from dotenv import load_dotenv
# load_dotenv()

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from langchain_mistralai import ChatMistralAI
# from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# # ── Same as chatbot.py ──
# model = ChatMistralAI(model="mistral-small-latest", temperature=0.9)
# message = [SystemMessage(content="You are a funny AI agent")]

# app = FastAPI()
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# class ChatRequest(BaseModel):
#     prompt: str

# @app.post("/chat")
# def chat(req: ChatRequest):
#     global message
#     message.append(HumanMessage(content=req.prompt))
#     response = model.invoke(message)
#     message.append(AIMessage(content=response.content))
#     return {"reply": response.content}

# @app.post("/reset")
# def reset():
#     global message
#     message = [SystemMessage(content="You are a funny AI agent")]
#     return {"ok": True}


from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# ── Models ──
model_global = ChatMistralAI(model="mistral-small-latest", temperature=0.9)
model_summarize = ChatMistralAI(model="mistral-small-latest", temperature=0.3)

# ── System prompts ──
GLOBAL_SYSTEM = "You are a helpful, funny, and friendly AI assistant. You can talk about anything — jokes, ideas, advice, coding, general knowledge. Be engaging and conversational."

SUMMARIZE_SYSTEM = """You are a professional Text Summarization Assistant.

Your task:
Extract and summarize any long-format text, story, article, or paragraph the user provides.

Rules:
- Do NOT add explanations or commentary outside the format
- Follow the exact output format below
- If information is missing → write NULL
- Keep the Short Summary to 3-4 lines max
- Do NOT guess or invent facts not in the text

Output Format:

Title (if detectable):
Main Topic:
Key Points:
  - 
  - 
  - 
Tone/Style:
Themes:

Short Summary:
"""

# ── Summarize prompt template ──
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", SUMMARIZE_SYSTEM),
    ("human", "Please summarize the following text:\n\n{text}")
])

# ── Conversation histories ──
global_history = [SystemMessage(content=GLOBAL_SYSTEM)]
summarize_history = [SystemMessage(content=SUMMARIZE_SYSTEM)]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    prompt: str
    mode: str = "global"  # "global" or "summarize"

@app.post("/chat")
def chat(req: ChatRequest):
    global global_history, summarize_history

    if req.mode == "summarize":
        # Use prompt template for summarization
        final_prompt = summarize_prompt.invoke({"text": req.prompt})
        response = model_summarize.invoke(final_prompt)
        # Also store in summarize history for context
        summarize_history.append(HumanMessage(content=req.prompt))
        summarize_history.append(AIMessage(content=response.content))
        return {"reply": response.content}
    else:
        # Global free-chat mode with full conversation memory
        global_history.append(HumanMessage(content=req.prompt))
        response = model_global.invoke(global_history)
        global_history.append(AIMessage(content=response.content))
        return {"reply": response.content}

@app.post("/reset")
def reset():
    global global_history, summarize_history
    global_history = [SystemMessage(content=GLOBAL_SYSTEM)]
    summarize_history = [SystemMessage(content=SUMMARIZE_SYSTEM)]
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok"}
