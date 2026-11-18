# 🤖 Mood AI Chatbot

A Streamlit chatbot where you choose the AI's **personality** (funny, angry, sad, or normal) from the sidebar. It remembers the whole conversation and is powered by **Llama 3.3 70B** on **Groq** through **LangChain**.

---

## Table of Contents
1. [Features](#features)
2. [Key concepts](#key-concepts)
3. [Tech stack](#tech-stack)
4. [Project structure](#project-structure)
5. [Setup](#setup)
6. [Usage](#usage)
7. [How it works](#how-it-works)
8. [Customization](#customization)
9. [Design decisions](#design-decisions)
10. [Limitations](#limitations)
11. [Troubleshooting](#troubleshooting)
12. [Future improvements](#future-improvements)

---

## Features
- 4 selectable moods, each with its own personality
- Multi-turn conversation with memory (follow-up questions work)
- Clean chat interface using Streamlit's chat components
- Chat resets automatically when the mood changes
- Safe "Angry" mode: sarcastic and grumpy, but never abusive
- Bonus: a simple terminal version (`cli_chatbot.py`)

| Mood | Behaviour |
|------|-----------|
| 😂 Funny | Humor, jokes and playful comments |
| 😡 Angry | Annoyed, grumpy and sarcastic, with no offensive language |
| 😢 Sad | Melancholic, emotional and gloomy |
| 🤖 Normal | Clear and professional |

---

## Key concepts

**LLMs are stateless.** The model doesn't remember earlier messages. To fake a conversation, the app stores a list of messages (system, human, AI) and sends the **entire list** with every request.

**System prompts define personality.** The first message in the list is a `SystemMessage` that tells the model how to behave. Swapping it changes the bot's mood without touching any other logic.

**Streamlit re-runs the script on every interaction.** Normal Python variables are lost each time, so the history lives in `st.session_state`, which persists between re-runs within a browser session.

---

## Tech stack

| Component | Technology | Role |
|-----------|-----------|------|
| Language | Python 3.9+ | Core language |
| LLM framework | LangChain (`langchain-core`) | Message classes and model interface |
| LLM provider | Groq API | Fast inference |
| Model | Llama 3.3 70B Versatile | Response generation |
| Web UI | Streamlit | Chat interface |
| Config | python-dotenv | Loads the API key from `.env` |

---

## Project structure

```
mood-chatbot/
├── app.py              # Streamlit mood chatbot (main app)
├── cli_chatbot.py      # Optional: simple terminal chatbot
├── requirements.txt    # Dependencies
├── .env.example        # Template for your API key
├── .gitignore          # Keeps secrets out of Git
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd mood-chatbot
```

### 2. (Recommended) Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Get a free key at [console.groq.com](https://console.groq.com), then:
```bash
cp .env.example .env        # Windows: copy .env.example .env
```
Edit `.env`:
```
GROQ_API_KEY=your_real_key_here
```
> ⚠️ Never commit `.env`. It is already listed in `.gitignore`.

---

## Usage

### Web app
```bash
streamlit run app.py
```
Open the URL shown in the terminal (usually http://localhost:8501), pick a mood in the sidebar and start chatting.

### Terminal version (optional)
```bash
python cli_chatbot.py
```
A minimal funny chatbot in the console. Enter `0` to quit.

---

## How it works

1. **Setup:** the app loads the API key and creates the `ChatGroq` model (`temperature=0.7`, `max_tokens=1024`).
2. **Mood selection:** a sidebar dropdown picks one of four system prompts stored in a dictionary.
3. **Mood change handling:** the current mood is stored in session state. If it differs from the selection, the history is replaced with a single new `SystemMessage` and the app re-runs. Resetting avoids mixing instructions from two different personalities.
4. **Displaying history:** every stored `HumanMessage` and `AIMessage` is rendered with `st.chat_message`. The `SystemMessage` is kept internal and not displayed.
5. **New message:** text from `st.chat_input` is appended as a `HumanMessage`, the full list goes to the model, and the reply is appended as an `AIMessage` and shown.

```
User picks mood ─► SystemMessage set ─► User types message
                                              │
              history = [System, Human, AI, Human, ...]
                                              │
                                  Groq Llama 3.3 70B ─► reply ─► appended to history
```

---

## Customization

**Add a new mood:** add an entry to the `system_prompts` dictionary and the sidebar options list in `app.py`:
```python
"🧙 Wizard": "You are an old wizard. Reply in a wise, mystical tone."
```
**Change the model:** edit the `model=` value to any Groq-hosted chat model.
**Adjust creativity:** `temperature` (0 = predictable, 1 = very creative) and `max_tokens` (reply length) are set where the model is created.

---

## Design decisions

- **Full message history per request:** the simplest reliable way to give a stateless model memory.
- **Reset on mood change:** prevents contradictory personalities in one conversation.
- **System prompts in a dictionary:** adding or editing moods needs no other code changes.
- **Streamlit session state:** keeps per-user history without a database.

---

## Limitations

- **History is unbounded.** Very long chats will eventually exceed the model's context window and slow down or fail.
- **Memory is temporary.** Refreshing or closing the tab loses the conversation.
- **No streaming.** Replies appear all at once after generation completes.
- **Persona strength varies.** Models sometimes drift out of character in long conversations.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Authentication / missing key error | Create `.env` (not just `.env.example`) containing your key. |
| `streamlit: command not found` | Activate your virtual environment and re-run `pip install -r requirements.txt`. |
| Bot ignores the mood | Re-select the mood in the sidebar; the chat resets and applies it. |
| Rate-limit errors | Wait a moment; the Groq free tier has usage limits. |

---

## Future improvements

- [ ] Stream responses token by token
- [ ] Trim or summarize long histories
- [ ] Let users write a custom persona
- [ ] Save and reload chat history
- [ ] Add a "Clear chat" button
- [ ] Deploy on Streamlit Community Cloud (store the key in Streamlit secrets)


