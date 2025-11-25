import streamlit as st
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import YouTubeSearchTool
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


prompt_template=PromptTemplate(
    template="""
    
    You are a helpful chat Assistant that answers /n 
    Query in a polite and respected way. If you don't
    answer to a query just respond with I don't know.
    Additionally, you have been given with a prompt.
    Please answer it as consice as posible.
    Also you have been given the message history till now

    Prompt:
    {prompt}

    Message History:
    {message_history}
    
    """,
    input_variables=['prompt','message_history']
)

st.title("Chat Bot (Gemini)")

if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []


@st.cache_resource
def load_gemini_model():
    return ChatGoogleGenerativeAI(
        model=st.session_state["gemini_model"],
        temperature=0.7
    )

model = load_gemini_model()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

chain = prompt_template | model | StrOutputParser()

if prompt := st.chat_input("What is up?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in chain.stream({'prompt': prompt , 'message_history':st.session_state.messages}):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.markdown(full_response)
    

    st.session_state.messages.append({"role": "assistant", "content": full_response})
