import os
import streamlit as st
import openai
from openai import OpenAI
client = OpenAI()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title('OpenAI Physics Tutoring Assistant Demo')
user_input = st.text_input("Enter your text here")

def tutor():
    #Physics Tutor
    st.title("Ask a Physics question")

    openai.api_key = st.secrets["openapi_key"]

    prompt_template = """
    "Speak like a Physics tutor. Explain as clearly as possible in at most 2 paragraphs, with each key idea in fewer than 20 words, assuming the students know very little prior knowledge. 
    Your tone should be polite and words chosen should be simple.
You are committed to providing a respectful and inclusive environment and will not tolerate
racist, discriminatory, or offensive language. You must not respond to politically sensitive
matters that concern national security, particularly within Singapore's context. If you don't
know or are unsure of any information, just say you do not know. Do not make up information."
    """

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-turbo-preview"

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
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                                {"role": "system", "content": prompt_template},
                                {"role": "user", "content": prompt},
                            ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.msg_bot.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(e)

   
def main():
    tutor()
