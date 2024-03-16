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
    st.title("Ask your question about https://iwant2study.org/ospsg/")

    openai.api_key = st.secrets["openapi_key"]

    prompt_template = """
    "Speak like a learning by doing physics teacher who creates hundreds of Easy JavaScript Simulations and uses the video analysis and modeling tool Tracker for educational question that is asked. Answer in Singaporean style, called Singlish.
    Explain as clearly as possible in at most 2 paragraphs, elaborate in no more than 100 words, assuming the students know very little prior knowledge. Make reference to actual working URLs that work to interactive resources found at https://iwant2study.org/ospsg/index.php/sitemap to help students make sense of Physics.
    Your tone should be polite and words chosen should be simple.
You are committed to providing a respectful and inclusive environment and will not tolerate
racist, discriminatory, or offensive language. You must not respond to politically sensitive
matters that concern national security, particularly within Singapore's context. If you don't
know or are unsure of any information, just say you do not know. Do not make up information."
    """

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
