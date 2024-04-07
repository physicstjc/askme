import os
import streamlit as st
from openai import OpenAI
# from openai import OpenAI
client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY'], 
)
import requests
from PIL import Image
import io

st.title("Physics Tutor")
st.text("Ask me a Physics question!")
#Change here onwards


def upload_image():
    """ Function to upload an image and return it """
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        return Image.open(io.BytesIO(bytes_data))
    return None

def analyze_image(image):
    """ Function to analyze the image using an AI model """
    # Assuming 'client' is your API client configured for the 'gpt-4-vision-preview'
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=300
    )

    if response.status_code == 200:
        # Handle and parse the response
        return response.json()  # Adjust based on actual response format
    else:
        raise Exception("Error in API response")


def display_results(results):
    """ Function to display the analysis results """
    st.write("Analysis Results:")
    st.write(results)

def main():
    st.title("Physics Question Analyzer using AI")
    
    image = upload_image()

    if image is not None:
        st.image(image, caption='Uploaded Image', use_column_width=True)
        if st.button('Analyze'):
            try:
                results = analyze_image(image)
                display_results(results)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
