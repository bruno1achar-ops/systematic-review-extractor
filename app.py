import streamlit as st
from google import genai
import json

st.title("Systematic Review Data Extractor")

# The new SDK automatically looks for the GEMINI_API_KEY environment variable
# set in your Streamlit Secrets.
try:
    client = genai.Client() # This handles the AQ key authentication
    model_id = "gemini-3.5-flash" # Use the latest model
except Exception as e:
    st.error(f"Authentication Error: {e}")
    st.stop()

user_fields = st.text_area("Fields to extract:", "Author, Year, Population")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # New SDK file handling
            file_bytes = uploaded_file.getvalue()
            
            response = client.models.generate_content(
                model=model_id,
                contents=[
                    {"mime_type": "application/pdf", "data": file_bytes},
                    f"Extract {user_fields} as JSON."
                ]
            )
            
            st.json(json.loads(response.text.replace('```json', '').replace('```', '')))
        except Exception as e:
            st.error(f"Error: {e}")
