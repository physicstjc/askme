import os
import boto3
import streamlit as st
from PIL import Image
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
from PIL import UnidentifiedImageError

s3_client = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

def upload_to_s3(uploaded_file):
    if uploaded_file is not None:
        file_name = uploaded_file.name
        uploaded_file.seek(0)  # Reset file pointer

        try:
            s3_client.upload_fileobj(uploaded_file, "askphysics", file_name)
            file_url = f"https://askphysics.s3.amazonaws.com/{file_name}"
            return file_url
        except Exception as e:
            st.error(f"Failed to upload to S3: {e}")
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

def main():
    st.title("Physics Tutor")
    st.text("Ask me a Physics question!")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            # Attempt to open the uploaded image file
            image = Image.open(io.BytesIO(uploaded_file.getvalue()))
            st.image(image, caption='Uploaded Image', use_column_width=True)
        except UnidentifiedImageError:
            st.error("The file you uploaded is not a valid image. Please upload a valid image file.")
            return  # Exit the function if the image is invalid
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return  # Exit the function in case of other errors
        if st.button('Analyze'):
            try:
                # Analyze the image using its URL
                results = analyze_image(file_url)
                display_results(results)
            except Exception as e:
                st.error(f"An error occurred: {e}")

def display_results(results):
    """ Function to display the analysis results """
    st.write("Analysis Results:")
    st.write(results)
	
if __name__ == "__main__":
    main()
