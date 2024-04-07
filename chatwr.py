import os
import streamlit as st
from openai import OpenAI
import boto3
from datetime import datetime
import csv
from datetime import datetime

# Initialize OpenAI
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Initialize AWS S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

# Function to store messages in AWS S3 bucket

# Function to store messages in a CSV file
def save_messages_to_csv(messages):
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_history_{timestamp}.csv"  # Added timestamp to filename

    # Write messages to CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for message in messages:
            writer.writerow([message['role'], message['content']])


st.title("Physics Socratic Tutor")
st.text("Let's get started. Ask me a Physics question!")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Speak like a teacher who asks socratic questions without giving the actual answers directly to the user. Help the user get to the answer by asking guiding questions to scaffold the learning"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
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
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    save_messages_to_csv(st.session_state.messages)
