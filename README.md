# ChatKaro — Streamlit Chat App

A lightweight Streamlit chat application that uses the Google Generative AI model (Gemini) via LangChain to answer user queries with streaming responses and a persistent in-session conversation history.

## Features

- Streamed assistant responses shown incrementally in the UI.
- Conversation history stored in session state.
- Configurable Gemini model name (default: `gemini-2.5-flash`).
- Easy to run locally with a single command.

## Prerequisites

- Python 3.8 or higher
- Internet access
- Google Generative AI API key (if using Google provider)

## Install

1. Create and activate a virtual environment:
   - Windows (PowerShell/CMD)
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS / Linux
     ```
     python -m venv venv
     source venv/bin/activate
     ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   If no requirements file is available, at minimum install:
   ```
   pip install streamlit python-dotenv langchain langchain-google-genai
   ```

## Setup

1. Create a `.env` file in the project root and add your API key if required by the provider:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   Do not commit `.env` to version control.

2. Confirm the model name in the app or change it at runtime via `st.session_state["gemini_model"]`.

## Run

From the project directory with the virtual environment active:
```
streamlit run streamlitApp.py
```
Open the URL shown in the terminal (usually http://localhost:8501).

## How it works (brief)

- The app builds a prompt template that includes the current message history.
- A cached Gemini model instance is created via `@st.cache_resource`.
- User messages are appended to `st.session_state.messages`.
- The chain (prompt → model → parser) streams chunks to the UI and updates message history.

## Configuration & Customization

- Change the default model:
  ```py
  st.session_state["gemini_model"] = "gemini-2.5-flash-lite"
  ```
- Replace the hardcoded prompt template to control assistant style and behavior.
- Add tools or agents (DuckDuckGo, YouTube, etc.) by integrating LangChain agents.

## Troubleshooting

- Authentication errors: verify the API key and restart the app.
- Missing packages: re-run `pip install -r requirements.txt`.
- Streaming or SDK errors: ensure compatible versions of LangChain and provider packages are installed.

## Suggestions

- Replace the current hardcoded prompt and message handling with more robust input sanitization.
- Persist chat history to disk or a simple database if long-term storage is desired.
- Add error handling and logging around model calls to improve reliability.
