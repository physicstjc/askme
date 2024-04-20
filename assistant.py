import os
import streamlit as st
import openai
import boto3
from datetime import datetime
import csv

# Initialize OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
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

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "system",
        "content": "Speak like a teacher who asks socratic questions without giving the actual answers directly to the user. Help the user get to the answer by asking guiding questions to scaffold the learning. Give responses that are no longer than 4 lines."
    }]

for message in st.session_state["messages"]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("What is up?")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        response_stream = client.completions.create(
            assistant_id="asst_iWWEKeASol9qFLldO7LnSW3t",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

  
    save_messages_to_csv_and_upload(st.session_state.messages, 'askphysics')
