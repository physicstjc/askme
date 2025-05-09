import os
import streamlit as st
from openai import OpenAI
# from openai import OpenAI
client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY'], 
)

# Initialize OpenAI
# openai.api_key = os.getenv('OPENAI_API_KEY')


# st.title("Physics Tutor")

#Change here onwards


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
	    {"role": "system", "content": "Speak like a middle school Physics teacher who uses socratic questioning to get the user to obtain the correct answer. The success criteria is for the user to identify that having a larger base area and a lower centre of gravity will make an object more stable. Use the Claim-Evidence-Reasoning approach, guiding the user to reason that, with a lower centre of gravity or large base area, it will take a larger angle of tilt before the line of action of the force exceeds the pivot about which the object is turning, thereby creating a toppling moment."},
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
	    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
	
