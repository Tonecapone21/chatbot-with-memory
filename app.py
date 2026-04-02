import os
from dotenv import load_dotenv
from pathlib import Path
import anthropic
import streamlit as st

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("AI Chatbot")
st.caption("Powered by Claude")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="You are a helpful assistant.",
        messages=st.session_state.messages
    )

    assistant_message = response.content[0].text

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_message)