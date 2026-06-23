import streamlit as st
import json
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="Extractor", layout="wide")
st.title("Systematic Review Data Extractor")

# FIX: Explicitly get the API key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not set in Streamlit Secrets!")
    st.stop()

# Initialize client with the key
client = genai.Client(api_key=api_key)

user_fields = st.text_area("Fields (comma separated):", "Author, Year, Population, Intervention, Outcome")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            pdf_bytes = uploaded_file.getvalue()
            
            prompt = f"Extract {user_fields} from this PDF. Return ONLY valid JSON."
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
                    prompt
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            
            data = json.loads(response.text)
            st.success("Extraction Complete!")
            st.json(data)
            
        except Exception as e:
            st.error(f"CRITICAL ERROR: {str(e)}")
