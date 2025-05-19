import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Read API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Missing API key! Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

# Configure Generative AI SDK
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Use correct model name (check access in your Google account)
model = gen_ai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Streamlit UI setup
st.set_page_config(page_title="Chat with Gemini", page_icon=":robot_face:")

def translate_role(role):
    return "assistant" if role == "model" else role

# Start chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("🤖 Gemini 1.5 Pro ChatBot")

# Show chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(translate_role(msg.role)):
        st.markdown(msg.parts[0].text)

# Input box
user_prompt = st.chat_input("Type your message...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")