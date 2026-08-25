import streamlit as st
from typing import cast

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from dotenv import load_dotenv


# -----------------------------
# Configuration
# -----------------------------

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Model
# -----------------------------

@st.cache_resource
def get_model():
    return ChatOpenAI(
        model="gpt-5.6-luna"
    )


model = get_model()


# -----------------------------
# Chat History
# -----------------------------

if "chat_history" not in st.session_state:

    history: list[BaseMessage] = [
        SystemMessage(
            content="You are a helpful assistant."
        )
    ]

    st.session_state.chat_history = history


# -----------------------------
# UI
# -----------------------------

st.title("🤖 AI Chatbot")

st.caption("Chat with your AI assistant")


# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.chat_history:

    # Don't display the system message
    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)


# -----------------------------
# User Input
# -----------------------------

user_input = st.chat_input("Type your message...")


if user_input:

    # Add user message to history
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = model.invoke(
                st.session_state.chat_history
            )

            response = result.content

            st.markdown(response)

    # Add AI response to history
    st.session_state.chat_history.append(
        AIMessage(content=response)
    )


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("Chat Settings")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.chat_history = [
            SystemMessage(
                content="You are a helpful assistant."
            )
        ]

        st.rerun()