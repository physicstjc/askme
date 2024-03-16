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


user_input = st.chat_input("What is up?")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Speak like a middle school Physics teacher for every question that was asked. Explain as clearly as possible, assuming the students know very little prior knowledge."},
    {"role": "user", "content": "{user_input}"}
  ]
)

full_response += response.choices[0].delta.get("content", "")
st.session_state.msg_bot.append({"role": "assistant", "content": "{full_response}"})

