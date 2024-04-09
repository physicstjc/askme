import os
import streamlit as st
from openai import OpenAI
import boto3
from datetime import datetime
import csv

# Initialize OpenAI
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize AWS S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])


def save_messages_to_csv_and_upload(messages, bucket_name):
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_history_{timestamp}.csv"

    # Write messages to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for message in messages:
            writer.writerow([message['role'], message['content']])

    # Upload file to S3
    s3.upload_file(Filename=filename, Bucket=bucket_name, Key=filename)


st.title("Practice with AI")
st.text("Which question would you like to discuss?")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Speak like a teacher who asks socratic questions without giving the actual answers directly to the user. Help the user get to the answer by asking guiding questions to scaffold the learning. Give responses that are no longer than 4 lines."}]


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# Generate and display response from AI
try:
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    for message in stream.messages():
        if message['role'] == 'assistant':
            response = message['content']
            with st.chat_message("assistant"):
                st.write(response)
            
            # Update chat history and save messages
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_messages_to_csv_and_upload(st.session_state.messages, 'askphysics')

except Exception as e:
    st.error(f"An error occurred: {e}")

  
    save_messages_to_csv_and_upload(st.session_state.messages, 'askphysics')
  
