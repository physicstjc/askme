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


def save_messages_to_csv_and_upload(messages, bucket_name):
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_history_{timestamp}.csv"

    # Write messages to CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for message in messages:
            writer.writerow([message['role'], message['content']])

    # Upload file to S3
    s3.upload_file(Filename=filename, Bucket=bucket_name, Key=filename)


st.title("Physics Experiment Planner")
st.text("Let's plan an investigation together")


# List of images
images = ["https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-ballinwater.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-ballwithmoremass.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-fanonboat.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-horseoncart.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-resultantforceattop.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-stopmoving.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-truckandcar.png"]
# Corresponding list of captions
captions = ["Image 1", "Image 2", "Image 3","Image 4","Image 5","Image 6","Image 7"]

# State for current image index
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0

# Button to go to the previous image
if st.button("Previous"):
    st.session_state.current_image = (st.session_state.current_image - 1) % len(images)

# Display the current image
st.image(images[st.session_state.current_image], width=300)
# Display caption for the current image
st.write(captions[st.session_state.current_image])

# Button to go to the next image
if st.button("Next"):
    st.session_state.current_image = (st.session_state.current_image + 1) % len(images)



# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": ""}]

# For planning assistant: Speak like a high school Physics teacher who who asks socratic questions without giving the actual answers directly. He will guide students to plan an experiment by asking probing questions such as identifying the independent and dependent variables, conditions to be kept constant, the ways to adjust the variables, the instruments to use and the type of graph to plot. Keep to simple laboratory equipment that is available in a normal science laboratory.
# For socratic tutor: Speak like a teacher who asks socratic questions without giving the actual answers directly to the user. Help the user get to the answer by asking guiding questions to scaffold the learning

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
    
    save_messages_to_csv_and_upload(st.session_state.messages, 'askphysics')
