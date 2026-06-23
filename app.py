import streamlit as st
from google import genai
import json

st.title("Data Extractor")

# Initialize the client. 
# It will automatically find GEMINI_API_KEY from your Streamlit Secrets.
try:
    client = genai.Client()
except Exception as e:
    st.error(f"Client init error: {e}")
    st.stop()

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # New SDK way to handle file uploads
            pdf_data = uploaded_file.getvalue()
            
            response = client.models.generate_content(
                model='gemini-2.0-flash', # Or your preferred model
                contents=[
                    {"mime_type": "application/pdf", "data": pdf_data},
                    "Extract the required fields and return as JSON."
                ]
            )
            
            st.json(json.loads(response.text.replace('```json', '').replace('```', '')))
        except Exception as e:
            st.error(f"Error: {e}")
