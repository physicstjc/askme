import os
import streamlit as st
from openai import OpenAI
import boto3
from datetime import datetime
import csv

# Initialize OpenAI


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
  
assistant = client.beta.assistants.create(
  name="Physics Tutor",
  instructions="You are a personal physics tutor. Write and run code to answer physics questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo",
)

# Initialize AWS S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

def save_messages_to_csv_and_upload(messages, bucket_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_history_{timestamp}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for message in messages:
            writer.writerow([message['role'], message['content']])
    s3.upload_file(Filename=filename, Bucket=bucket_name, Key=filename)

st.title("Practice with AI")
st.text("Which question would you like to discuss?")

thread = client.beta.threads.create()

user_input = st.chat_input("What is up?")
if user_input:
    message = client.beta.threads.messages.create(
        role="user",
        content="user_input"
    )

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=asst_iWWEKeASol9qFLldO7LnSW3t
)
    save_messages_to_csv_and_upload(st.session_state.messages, 'askphysics')
