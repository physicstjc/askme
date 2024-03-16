import os
import streamlit as st
from openai import OpenAI
# from openai import OpenAI
client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY'], 
)

# Initialize OpenAI
# openai.api_key = os.getenv('OPENAI_API_KEY')


st.title("Physics Tutor")
if 'msg_bot' not in st.session_state:
    st.session_state.msg_bot = []

myinput = st.text_input("What is up?")  # Use text_input instead of chat_input for compatibility

if myinput:
    st.session_state.msg_bot.append({"role": "user", "content": myinput})

    with st.container():  # Use container for grouping elements
        st.write("User:", myinput)

    # Create the response from the model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Speak like a middle school Physics teacher for every question that was asked. Explain as clearly as possible, assuming the students know very little prior knowledge."},
            {"role": "user", "content": myinput},
        ],
    )

    # Check response validity and display
    if response and 'choices' in response and response.choices and len(response.choices) > 0 and 'message' in response.choices[0]:
        with st.container():  # Use container for grouping elements
            st.write("Assistant:", response.choices[0].message.content)
