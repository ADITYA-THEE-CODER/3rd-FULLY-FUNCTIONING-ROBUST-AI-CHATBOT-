import streamlit as st
from groq import Groq
import os

# Load API key from Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Title
st.title("🤖 AI Chatbot")

# Initialize memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.chat_history
        )

        bot_reply = response.choices[0].message.content

        # Display bot reply
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        # Save bot reply
        st.session_state.chat_history.append(
            {"role": "assistant", "content": bot_reply}
        )

    except Exception as e:
        st.error(f"Error: {e}")
