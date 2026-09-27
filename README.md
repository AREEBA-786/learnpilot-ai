# 🧭 Learning Path Generator — Agentic AI with Model Context Protocol (MCP)

An **agentic AI application** that turns any learning goal into a structured, day-wise learning path — autonomously. Built with **LangGraph's ReAct agent framework** and the **Model Context Protocol (MCP)**, the agent reasons about the goal, decides which tools to call, curates relevant YouTube videos, and publishes the final plan directly to Google Drive or Notion — all through a persistent, ChatGPT-style chat interface.

## Features

- 🧠 Autonomous agent orchestration via LangGraph + Gemini 2.5 Flash
- 🎥 YouTube integration for curated video resources
- 📁 Google Drive / 📝 Notion integration for document publishing
- 💬 Persistent, multi-session chat interface (start new chats, revisit and delete past sessions)
- 🚀 Real-time streaming progress updates while the agent works
- 🎨 Custom-themed, distraction-free UI

## Architecture
User Goal → Streamlit Chat UI → LangGraph ReAct Agent (Gemini 2.5 Flash)
│
┌──────────────┼──────────────┐
YouTube MCP Drive MCP Notion MCP
(via Pipedream)

## Tech Stack

| Layer | Technology |
|---|---|
| Agent framework | LangGraph (`create_react_agent`) — ReAct-style reasoning |
| LLM | Google Gemini 2.5 Flash |
| Tool integration | Model Context Protocol (MCP) via LangChain MCP Adapters, over Pipedream |
| UI | Streamlit (chat interface, session persistence) |
| Persistence | JSON-based local chat session storage |

## Prerequisites

- Python 3.10+
- A Gemini API key (free) from [Google AI Studio]
- Pipedream MCP URLs for YouTube (required) and either Google Drive or Notion

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AREEBA-786/mcp-learning-path-demo.git
cd mcp-learning-path-demo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

No secrets are hardcoded — everything is entered securely in the sidebar at runtime:

1. **Gemini API Key** — from Google AI Studio
2. **Pipedream URL for YouTube** (required)
3. **Pipedream URL for Google Drive or Notion** (based on your preference)

## Running the Application

```bash
streamlit run app.py
```
The app will be available at `http://localhost:8501`.

## Usage

1. Enter your Gemini API key and Pipedream URLs in the sidebar.
2. Choose your secondary tool (Drive or Notion).
3. Type your learning goal in the chat box, e.g.:
   - *"I want to learn python basics in 3 days"*
   - *"I want to learn data science basics in 10 days"*
4. The agent autonomously plans the path, finds videos, publishes the document, builds the playlist, and returns both links.
5. Start a **New Chat** anytime — every session is saved and can be revisited or deleted from the sidebar.

## Project Structure
├── app.py # Chat UI, session management, styling
├── utils.py # Agent setup and orchestration logic (LangGraph + MCP)
├── prompt.py # System prompt for the agent
├── chat_store.py # Persistent chat session storage (JSON)
├── requirements.txt # Project dependencies
└── .streamlit/
└── config.toml # Theme configuration
