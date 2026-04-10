import streamlit as st
from groq import Groq

# Title
st.title("🤖 Aditya's AI Chatbot")

# Create client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": "You are a smart, concise AI assistant who explains clearly like a teacher."
        }
    ]

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

# Handle user input
if user_input and user_input.strip() != "":
    
    # Store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Loading indicator
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.chat_history
            )

        bot_reply = response.choices[0].message.content

        # Show bot reply
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        # Store bot reply
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

    except Exception as e:
        st.error(f"Error: {e}")
