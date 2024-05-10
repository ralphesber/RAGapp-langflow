import streamlit as st
from langflow import run_flow_from_json

def main():
    # Get user input
    message = st.text_input("Enter message:")

    if message:
        # Run the flow with the user's input
        inputs = {"question": message}
        response = run_flow_from_json(flow="Sample.json",
                                input_value=inputs
        # Display the result
        st.write(result)

if __name__ == "__main__":
    main()