import streamlit as st
import json
import time
from google import genai
from google.genai import types

# 1. UI Configuration
st.set_page_config(page_title="Research Data Extractor", layout="wide")
st.title("Systematic Review Data Extractor")

# 2. Setup Client
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"API Key issue: {e}")
    st.stop()

# 3. Dynamic Schema Definition
st.subheader("Define Your Fields")
user_fields = st.text_area("Enter fields to extract (comma separated):", 
                          "Author, Year, Population, Intervention, Outcome")
schema_list = [f.strip() for f in user_fields.split(",")]

# 4. File Upload
uploaded_file = st.file_uploader("Upload Study PDF", type="pdf")

# 5. Extraction Pipeline
if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing document..."):
        try:
            # Read file as bytes
            bytes_data = uploaded_file.getvalue()
            
            # Upload to Gemini File API
            pdf_file = client.files.upload(
                file=bytes_data, 
                config={'display_name': uploaded_file.name, 'mime_type': 'application/pdf'}
            )
            
            # Wait for processing
            while pdf_file.state.name == "PROCESSING":
                time.sleep(2)
                pdf_file = client.files.get(name=pdf_file.name)
            
            # Formulate structured prompt
            prompt = f"Extract {schema_list} from this PDF. Return strictly as a JSON object."
            
            # Generate structured response
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[pdf_file, prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            
            # Display Results
            data = json.loads(response.text)
            st.success("Extraction Complete!")
            st.json(data)
            
            # Download trigger
            st.download_button(
                label="Download JSON Data",
                data=json.dumps(data, indent=4),
                file_name="extracted_data.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error during extraction: {str(e)}")
