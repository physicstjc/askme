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

myinput = st.chat_input("What is up?", key="my_unique_chat_input_key")

if myinput:
    st.session_state.msg_bot.append({"role": "user", "content": myinput})
    
    with st.chat_message("user"):
        st.markdown(myinput)


    # Create the response from the model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Speak like a middle school Physics teacher for every question that was asked. Explain as clearly as possible, assuming the students know very little prior knowledge."},
            {"role": "user", "content": myinput},
        ],
        stream=True,  # or False, depending on your requirement
    )

    # Ensure response is valid and then display it
    if response and response.choices and response.choices[0] and response.choices[0].message:
        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message.content)
