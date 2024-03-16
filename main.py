import os
import streamlit as st
import openai
from openai import OpenAI
client = OpenAI()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title('OpenAI GPT-4 Physics Tutoring Assistant Demo')
user_input = st.text_input("Enter your text here")

if user_input:
    # Get response from OpenAI GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful AI tutoring assistant..."},
            {"role": "user", "content": "${user_input}"}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Display the response
    if response:
        st.write(response.choices[0].message['content'])
