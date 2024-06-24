__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import logging
import sys
import time
from typing import Optional
import requests
import json
import streamlit as st
# from streamlit_chat import message
import logging
from typing import Optional
import requests
import os
import re
from dotenv import load_dotenv

try:
    from langflow.load import run_flow_from_json
except ImportError as e:
    st.error(f"ImportError: {e}")
    st.stop()
# Load environment variables from .env file if it exists
load_dotenv()


def load_secrets():
    
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    token = os.getenv('token')
    api_endpoint = os.getenv('api_endpoint')

    # Load and modify the flow.json file
    with open('Langflow sample.json', 'r') as file:
        flow_config = json.load(file)

    flow_config['openai_api_key'] = openai_api_key


TWEAKS = {
  "OpenAIModel-e49CE": {},
  "ChatOutput-jsKKh": {},
  "ChatInput-FzQxA": {},
  "Prompt-LmpqH": {},
  "AstraDBSearch-7oXhE": {},
  "OpenAIEmbeddings-wSUIF": {},
  "Prompt-poPXn": {},
  "OpenAIModel-oIQER": {}
}

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)


BASE_AVATAR_URL = (
    "https://raw.githubusercontent.com/garystafford-aws/static-assets/main/static"
)


def main():
    st.set_page_config(page_title="Teacher Assistant")
    load_secrets()
    st.markdown("##### Welcome to the teacher assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if prompt := st.chat_input("I'm your virtual teacher assistant, how may I help you?"):
        # Add user message to chat history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "avatar": f"{BASE_AVATAR_URL}/people-64px.png",
            }
        )
        # Display user message in chat message container
        with st.chat_message(
            "user",
            avatar=f"{BASE_AVATAR_URL}/people-64px.png",
        ):
            st.write(prompt)

        # Display assistant response in chat message container
        with st.chat_message(
            "assistant",
            avatar=f"{BASE_AVATAR_URL}/bartender-64px.png",
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(prompt)
                message_placeholder.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": f"{BASE_AVATAR_URL}/bartender-64px.png",
            }
        )

def generate_response(prompt):
    logging.info(f"question: {prompt}")
    inputs = {"question": prompt}
    response = run_flow_from_json(flow="Langflow sample.json",
                                input_value=prompt, tweaks=TWEAKS)
    try:
        return response[0].outputs[0].messages[0].message
    except json.JSONDecodeError as e:
        logging.error (f"JSON decode error: {e}")
        return "Sorry, there was a problem finding an answer for you."
    except Exception as e:
        logging.error (f"An unexpected error occurred: {e}")
        return "Sorry, there was a problem finding an answer for you."


if __name__ == "__main__":
    main()