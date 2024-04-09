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


st.title("Argue with AI")
st.text("Which image would you like to discuss?")
st.text("e.g. type 'Image 1' if you want to discuss the first image.")

# List of images
images = ["https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-ballwithmoremass.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-fanonboat.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-horseandcart.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-resultantforceattop.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-stopmoving.png", "https://askphysics.s3.ap-southeast-1.amazonaws.com/argue-truckandcar.png"]
# Corresponding list of captions
captions = ["Image 1", "Image 2", "Image 3","Image 4","Image 5","Image 6"]

# State for current image index
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0

# Display the current image
current_index = st.session_state.current_image
if 0 <= current_index < len(images):
    st.image(images[current_index], width=300)
    st.write(captions[current_index])


# Button to go to the previous image
if st.button("Previous"):
    st.session_state.current_image = (st.session_state.current_image - 1) % len(images)
# Button to go to the next image
if st.button("Next"):
    st.session_state.current_image = (st.session_state.current_image + 1) % len(images)

if "image_descriptions" not in st.session_state:
    st.session_state.image_descriptions = {
        "Image 1": "A cartoon that shows a boy saying that a heavier object will fall faster because it has more mass, when in fact, both objects should reach the ground at the same time if air resistance is negligible.",
        "Image 2": "A boy is on a boat with a fan attached to the boat that is blow on a sail. The boy assumed that the fan and move the sailboat forward. However, this is a misconception as the backward force exerted by the wind on the fan is equal in magnitude to the forward force exerted by the wind on the sail.",
        "Image 3": "A horse with a cart harnessed to it is cannot move as the cart is pulling it back with the same force that the horse is exerted on the cart. This is a misunderstanding of Newton's third law, as the action-reaction forces act on different bodies and hence, do not cancel each other out.",
        "Image 4": "A boy watches a ball being thrown upward and assumes that at the top, the ball is experiences no resultant force as it is stationary. On the contrary, the ball still experiences its weight and hence, is able to continue its acceleration, thus making its way down thereafter.",
        "Image 5": "A boy is speaking to his teacher saying that if a rocket in space runs out of fuel, it will come to a stop. However, there are no dissipative forces in space so by Newton's First law, the rocket will continue its motion even if there is no force acting on it.",
        "Image 6": "A boy claims that a truck which has more mass than a car, is exerting a larger force on the car during collision. However, this violates Newton's third law, which states that the forces are equal in magnitude.",
    }

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Speak like a teacher who asks socratic questions without giving the actual answers directly to the user. Help the user get to the answer by asking guiding questions to scaffold the learning. The user will be prompted for an image which he would like to discuss. Question the user on whether he thinks the child's understanding is correct and ask for his assumptions. Give responses that are no longer than 4 lines."}]

# For planning assistant: Speak like a high school Physics teacher who who asks socratic questions without giving the actual answers directly. He will guide students to plan an experiment by asking probing questions such as identifying the independent and dependent variables, conditions to be kept constant, the ways to adjust the variables, the instruments to use and the type of graph to plot. Keep to simple laboratory equipment that is available in a normal science laboratory.
# For socratic tutor: Speak like a teacher who asks socratic questions without giving the actual answers directly to the user. Help the user get to the answer by asking guiding questions to scaffold the learning

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What do you think?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check for image prompt and handle descriptions
    if prompt.lower().startswith("image"):
        image_number = prompt.split()[1] if len(prompt.split()) > 1 else None
        if image_number and image_number.isdigit():
            image_key = "Image " + image_number
            image_description = st.session_state.image_descriptions.get(image_key, "No description available.")
            st.session_state.messages.append({"role": "system", "content": image_description})
  
    # Generate and display response from AI
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=False,
    )
    response = stream.choices[0].message['content']
    with st.chat_message("assistant"):
        st.write(response)
    
    # Update chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_messages_to_csv_and_upload(st.session_state.messages, 'askphysics')



