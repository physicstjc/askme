import os
import streamlit as st
import openai
from openai import OpenAI
client = OpenAI()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title('OpenAI Physics Tutoring Assistant Demo')
user_input = st.text_input("Enter your text here")

assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

import time
  
while run.status in ['queued', 'in_progress', 'cancelling']:
  time.sleep(1) # Wait for 1 second
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)
