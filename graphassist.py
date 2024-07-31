import streamlit as st
import openai
import json

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to call OpenAI API and get JavaScript code
def get_js_code(description):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate a JavaScript code using Plotly.js to plot a graph for the following motion description: {description}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    js_code = response.choices[0].text.strip()
    return js_code

st.title('Motion Description to Plotly.js Graph')

description = st.text_area('Enter a description of the motion:')

if st.button('Generate Graph'):
    if description:
        js_code = get_js_code(description)
        st.subheader('Generated JavaScript Code:')
        st.code(js_code, language='javascript')

        # Embedding the Plotly.js graph
        st.subheader('Plotly.js Graph:')
        html_code = f"""
        <div id="plotly-div"></div>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
        {js_code}
        </script>
        """
        st.components.v1.html(html_code, height=600)
    else:
        st.error('Please enter a description of the motion.')

