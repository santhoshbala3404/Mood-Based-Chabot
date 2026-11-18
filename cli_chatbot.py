"""Command-line chatbot with conversation memory.

Run:
    python cli_chatbot.py
"""
import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise SystemExit("GROQ_API_KEY missing. Copy .env.example to .env and add your key.")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key,
    temperature=0.7,
    max_tokens=1024,
)

messages = [SystemMessage(content="You are a funny AI agent.")]

print("Chatbot is ready! Ask your question. Enter 0 to quit.")
while True:
    prompt = input("Enter the question: ").strip()
    if prompt == "0":
        break
    if not prompt:
        continue

    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print(f"Bot: {response.content}")
