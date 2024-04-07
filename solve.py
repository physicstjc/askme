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
import tempfile
import shutil

def upload_image():
    """ Function to upload an image and return it """
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        return Image.open(io.BytesIO(bytes_data))
    return None

def analyze_image(image_url):
    """ Function to analyze the image using an AI model """
    try:
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
            return response.json()  # Adjust based on actual response format
        else:
            # Detailed error message
            st.write("API response error: ", response.json())
            raise Exception("Error in API response")
    except Exception as e:
        # Detailed exception message
        st.error(f"An error occurred: {str(e)}")
        return None

def display_results(results):
    """ Function to display the analysis results """
    st.write("Analysis Results:")
    st.write(results)

def main():
    st.title("Physics Question Analyzer using AI")
    
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(io.BytesIO(uploaded_file.getvalue()))
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Construct the URL for the uploaded image
        base_url = "https://solvephy.streamlit.app/~/+/media/"
        image_url = f"{base_url}{uploaded_file.name}"

        # Analyze the image when the button is clicked
        if st.button('Analyze'):
            try:
                results = analyze_image(image_url)
                display_results(results)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
