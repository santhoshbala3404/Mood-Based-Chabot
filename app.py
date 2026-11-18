from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st
import os

load_dotenv()

# Initialize model
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
    max_tokens=1024
)

# Page Config
st.set_page_config(page_title="Mood AI Chatbot", page_icon="🤖")
st.title("🤖 Mood AI Chatbot")

# ==========================
# Mood Selector
# ==========================
mood = st.sidebar.selectbox(
    "Choose Bot Mood",
    ["😂 Funny", "😡 Angry", "😢 Sad", "🤖 Normal"]
)

# Define system prompts
system_prompts = {
    "😂 Funny": (
        "You are a funny AI assistant. "
        "Answer every question with humor, jokes, and playful comments."
    ),
    "😡 Angry": (
        "You are an angry AI assistant. "
        "Reply in an annoyed, grumpy, and sarcastic tone, but never use abusive or offensive language."
    ),
    "😢 Sad": (
        "You are a sad AI assistant. "
        "Reply in a melancholic, emotional, and slightly gloomy tone."
    ),
    "🤖 Normal": (
        "You are a helpful AI assistant. "
        "Answer clearly and professionally."
    )
}

# ==========================
# Initialize Chat History
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update system message when mood changes
# Reset chat when mood changes
if (
    "current_mood" not in st.session_state
    or st.session_state.current_mood != mood
):
    st.session_state.current_mood = mood

    # Clear entire conversation and start fresh
    st.session_state.messages = [
        SystemMessage(content=system_prompts[mood])
    ]

    st.rerun()
# If no system message exists
if not st.session_state.messages or not isinstance(
    st.session_state.messages[0],
    SystemMessage
):
    st.session_state.messages.insert(
        0,
        SystemMessage(content=system_prompts[mood])
    )

# ==========================
# Display Chat History
# ==========================
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# ==========================
# Chat Input
# ==========================
prompt = st.chat_input("Ask me anything...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.spinner("Thinking..."):
        response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    with st.chat_message("assistant"):
        st.write(response.content)