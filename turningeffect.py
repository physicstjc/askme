import os
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
# from openai import OpenAI
client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY'], 
)

# Initialize OpenAI
# openai.api_key = os.getenv('OPENAI_API_KEY')


# st.title("Physics Tutor")

#Change here onwards
st.markdown("Interact with the app and observe how the height and width affects how far the object must tilt before it topples.")
components.html(
    """
    <iframe scrolling="no" title="Stability" src="https://www.geogebra.org/material/iframe/id/hp777myf/width/640/height/480/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false" width="640px" height="480px" style="border:0px;"> </iframe>
    """,
    height=480  # This is needed to ensure the iframe is shown
)
st.markdown("Let's chat with the AI bot! Start by typing your observations in the space below.")
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
	    {"role": "system", "content": "Speak like a middle school Physics teacher who uses socratic questioning to get the user to obtain the correct answer. The success criteria is for the user to identify that having a larger base area and a lower centre of gravity will make an object more stable. Use the Claim-Evidence-Reasoning approach, guiding the user to reason that, with a lower centre of gravity or large base area, it will take a larger angle of tilt before the line of action of the force exceeds the pivot about which the object is turning, thereby creating a toppling moment. Congratulate the user once he has achieved the success criteria and end the conversation politely"},
    ]

# Display chat messages from history on app rerun (excluding system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("Your input here"):
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
	
