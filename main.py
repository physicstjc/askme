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

myinput = st.chat_input("What is up?")

try:
	if myinput := st.chat_input("What is up?"):
		st.session_state.msg_bot.append({"role": "user", "content": myinput})
		with st.chat_message("user"):
			st.markdown(myinput)

		with st.chat_message("assistant"):
			message_placeholder = st.empty()
			response = client.chat.completions.create(
  				model="gpt-3.5-turbo",
  				messages=[
					{"role": "system", "content": "Speak like a middle school Physics teacher for every question that was asked. Explain as clearly as possible, assuming the students know very little prior knowledge."},
					{"role": "user", "content": myinput},
				],
				stream=True,
			)

st.markdown(response.choices[0].message.content)

