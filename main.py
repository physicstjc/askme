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

#Change here onwards
if 'msg_bot' not in st.session_state:
    st.session_state.msg_bot = []

myinput = st.text_input("What is up?")  # Replace with chat_input if available

if myinput:
    st.session_state.msg_bot.append({"role": "user", "content": myinput})

    with st.container():  # Display user input
        st.write("User:", myinput)

    try:
        # Create the response from the model
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Speak like a middle school Physics teacher for every question that was asked. Explain as clearly as possible, assuming the students know very little prior knowledge."},
                {"role": "user", "content": myinput},
            ],
        )

        # Debug print
# Display user's input
	st.write(f"User: {myinput}")
	
	# Check if the response is valid and display the assistant's response
	if response and response.choices and response.choices[0] and response.choices[0].message:
	    assistant_response = response.choices[0].message.content
	    st.write(f"Assistant: {assistant_response}")
	
    	except Exception as e:
        	st.error(f"An error occurred: {e}")
