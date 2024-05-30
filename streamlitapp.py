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
from dotenv import load_dotenv
# from langflow import run_flow_from_json
try:
    from langflow.load import run_flow_from_json
except ImportError as e:
    st.error(f"ImportError: {e}")
    st.stop()
# Load environment variables from .env file if it exists
load_dotenv()


openai_api_key = os.getenv('openai_api_key')
token = os.getenv('token')
api_endpoint = os.getenv('api_endpoint')

# Load and modify the flow.json file
with open('Langflow sample.json', 'r') as file:
    flow_config = json.load(file)

flow_config['openai_api_key'] = openai_api_key
flow_config['token'] = token
flow_config['api_endpoint'] = api_endpoint



log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "https://ralphkognity-langflow-preview.hf.space/api/v1/run"
FLOW_ID = "7e840d19-3197-49e9-846c-b553943e02ab"
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
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
BASE_AVATAR_URL = (
    "https://raw.githubusercontent.com/garystafford-aws/static-assets/main/static"
)


def main():
    st.set_page_config(page_title="Teacher Assistant")

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


def run_flow(message: str, flow_id: str, output_type: str = "chat", input_type: str = "chat", tweaks: Optional[dict] = None, api_key: Optional[str] = None) -> dict:
    
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param flow_id: The ID of the flow to run
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def generate_response(prompt):
    logging.info(f"question: {prompt}")
    inputs = {"question": prompt}
    #response = run_flow(prompt, flow_id=FLOW_ID, tweaks=TWEAKS)
    response = run_flow_from_json(flow="Langflow sample.json",
                                input_value=prompt)
    try:
        # logging.info(f"answer: {response['outputs'][0]['outputs'][0]['results']['result']}")
        # return response['outputs'][0]['outputs'][0]['results']['result']
        return response[0]
    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."


if __name__ == "__main__":
    main()