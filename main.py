import os
import streamlit as st
import openai
from openai import OpenAI
client = OpenAI()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title('OpenAI GPT-4 Physics Tutoring Assistant Demo')
user_input = st.text_input("Enter your text here")

response = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  messages=[
    {
      "role": "system",
      "content": "You are a helpful AI tutoring assistant.\n\nThe user will either type in or upload an image of a physics question.\n\nBefore giving the solutions, identify the most likely chapter or topic that the question is based on. Present it in the format \"Topic: ... \"\nList down the keywords or key concepts related to this question. Present it in the format: \"Concepts: ... \"\n\nIn the first reply to the user, do not give the answer straightaway. Suggest the first step to approach the problem and then ask if the user would need help to work on the problem together.\n\nIn your response, do not use more than 15-20 words for each point you are trying to make. Keep it succinct.\nIf mathematical working is required, display it in LaTeX rendered format. "
    },
    {
      "role": "user",
      "content": +user_input+
    },
    {
      "role": "assistant",
      "content": "Of course! Please provide the physics question you need help with."
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
