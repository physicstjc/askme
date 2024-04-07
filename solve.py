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
import io
import tempfile
import shutil
from PIL import UnidentifiedImageError

s3_client = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

def upload_to_s3(uploaded_file, bucket_name, object_name=None):

    if object_name is None:
        object_name = uploaded_file.name

    uploaded_file.seek(0)  # Reset file pointer
    try:
        # Upload the file
        s3_client.upload_fileobj(uploaded_file, "askphysics", object_name)
        return f"https://askphysics.s3.ap-southeast-1.amazonaws.com/{object_name}"
    except Exception as e:
        print(e)
        return None

def analyze_image(image_url):
    """ Function to analyze the image using an AI model """
    try:
	print("Image URL being analyzed:", image_url)  
	
	# For debugging
	    
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
            max_tokens=600
        )

        if response.status_code == 200:
            return response.json()  # Adjust based on actual response format
        else:
            # Detailed error message
            print("API Response Error:", response.json())  # Log the error response
            raise Exception("Error in API response")
    except Exception as e:
        # Detailed exception message
        st.error(f"An error occurred: {str(e)}")
        return None
def main():
    st.title("Physics Tutor")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # To see details
        # file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        # st.write(file_details)

        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Upload to S3
        s3_bucket_name = "askphysics"  # replace with your bucket name
        file_url = upload_to_s3(uploaded_file, s3_bucket_name)
        # if file_url:
        #    st.success(f"Uploaded to S3 at URL: {file_url}")
        # else:
        #    st.error("Failed to upload to S3.")

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
