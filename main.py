import streamlit as st
import openai

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit UI
st.title('OpenAI GPT-3 Demo')

user_input = st.text_input("Enter your text here")

if st.button('Generate'):
    response = openai.Completion.create(
      engine="text-davinci-003",  # or any other GPT model
      prompt=user_input,
      max_tokens=50
    )

    st.write(response.choices[0].text.strip())
