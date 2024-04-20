import os
import streamlit as st
from openai import OpenAI
import boto3
from datetime import datetime
import csv

# Initialize OpenAI


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
assistant = openai_client.beta.assistants.retrieve(
    "asst_iWWEKeASol9qFLldO7LnSW3t"
)
# ASSISTANT_ID = "asst_iWWEKeASol9qFLldO7LnSW3t"

st.title("Practice with AI")
st.text("Which question would you like to discuss?")

user_input = st.chat_input("What is up?")
if user_input:
    thread = client.beta.threads.create(
        message=[
            {
                "role": "user",
                "content": [user_input],
            }
        ]
    )

    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        assistant_id=assistant.id,
      )
    
    # Check periodically whether the run is done, and update the status
    while run.status != "completed":
        time.sleep(5)
        status_box.update(label=f"{run.status}...", state="running")
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

    # Once the run is complete, update the status box and show the content
    status_box.update(label="Complete", state="complete", expanded=True)
    messages = openai_client.beta.threads.messages.list(
        thread_id=thread.id
    )
    st.markdown(messages.data[0].content[0].text.value)
  
