import streamlit as st
import json
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="Extractor", layout="wide")
st.title("Systematic Review Data Extractor")

# Setup Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Check API Key in Secrets.")
    st.stop()

user_fields = st.text_area("Fields (comma separated):", "Author, Year, Population, Intervention, Outcome")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # UPLOAD: Using the file object directly with the API
            # Note: We are not using the File API's 'upload' if it's causing issues.
            # Instead, we pass the file content directly.
            pdf_bytes = uploaded_file.getvalue()
            
            # Using the model directly with file bytes
            prompt = f"Extract {user_fields} from this PDF. Return ONLY valid JSON."
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Part.from_bytes(
                        data=pdf_bytes,
                        mime_type='application/pdf'
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            
            data = json.loads(response.text)
            st.success("Extraction Complete!")
            st.json(data)
            
        except Exception as e:
            st.error(f"CRITICAL ERROR: {str(e)}")
            st.exception(e) # This will show the full traceback on the screen
