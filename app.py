import streamlit as st
from google import genai
import json

st.title("Data Extractor")

# The new SDK automatically detects 'GEMINI_API_KEY' from Streamlit Secrets
try:
    client = genai.Client()
except Exception as e:
    st.error(f"Client init error: {e}")
    st.stop()

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
user_fields = st.text_area("Fields to extract:", "Author, Year, Population")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # Upload file correctly to the new SDK's file service
            temp_file = client.files.upload(
                file=uploaded_file,
                config={"mime_type": "application/pdf"}
            )
            
            prompt = f"Extract {user_fields} as JSON."
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[temp_file, prompt]
            )
            
            # Clean and display
            clean_text = response.text.replace('```json', '').replace('```', '')
            st.json(json.loads(clean_text))
            
            # Clean up uploaded file
            client.files.delete(name=temp_file.name)
            
        except Exception as e:
            st.error(f"Error: {e}")
