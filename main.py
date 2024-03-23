import os
import streamlit as st
from openai import OpenAI
# from openai import OpenAI
client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY'], 
)

# Initialize OpenAI
# openai.api_key = os.getenv('OPENAI_API_KEY')


st.title("Physics Tutor")
st.text("Ask me a Physics question!")
#Change here onwards

u
# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Read the image file
    image_data = uploaded_file.getvalue()

    # Process the image with the GPT-4-Vision-Preview model
    response = client.image_model.process(
        model="gpt-4-vision-preview",
        image_data=image_data
    )

    # Display results
    st.write(response)
	
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Speak like a friend who is very good in physics. Explain in a succinct and clearly manner, with no more than 15 words per key idea, assuming the students know very little prior knowledge. Display answers with mathematical content using LaTeX markup for clear and precise presentation. Ensure all equations, formulas, and mathematical expressions are correctly formatted in LaTeX."},]

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
            model="gpt-4-turbo-preview",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
	
