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

response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt-template="Speak like a middle school Physics teacher for every question that was asked. Explain as clearly as possible, assuming the students know very little prior knowledge."
)


if "openai_model" not in st.session_state:
	st.session_state["openai_model"] = "gpt-3.5-turbo"

if "msg_bot" not in st.session_state:
	st.session_state.msg_bot = []

for message in st.session_state.msg_bot:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

try:

	if prompt := st.chat_input("What is up?"):
		st.session_state.msg_bot.append({"role": "user", "content": prompt})
		with st.chat_message("user"):
			st.markdown(prompt)

		with st.chat_message("assistant"):
			message_placeholder = st.empty()
			full_response = ""
			for response in client.completions.create(
				model="gpt-3.5-turbo",
				messages=[
					{"role": "system", "content": "{prompt-template}"},
					{"role": "user", "content": "{prompt}"},
				],
				stream=True,
			):
				full_response += response.choices[0].delta.get("content", "")
				message_placeholder.markdown(full_response + "▌")
			message_placeholder.markdown(full_response)
		st.session_state.msg_bot.append({"role": "assistant", "content": full_response})

except Exception as e:
	st.error(e)
