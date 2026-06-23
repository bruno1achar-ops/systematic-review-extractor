import streamlit as st
from google import genai
import json

st.title("Data Extractor")

# Initialize client. The SDK automatically detects 'GEMINI_API_KEY' 
# from your Streamlit Secrets.
try:
    client = genai.Client()
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()

# Get fields from user and file
user_fields = st.text_area("Fields to extract (comma separated):", "Author, Year, Population")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # 1. Upload the file correctly
            # The new SDK handles the PDF binary data automatically
            temp_file = client.files.upload(
                file=uploaded_file,
                config={"mime_type": "application/pdf"}
            )
            
            # 2. Call the model using the file object
            prompt = f"Extract these fields: {user_fields}. Return ONLY valid JSON."
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[temp_file, prompt]
            )
            
            # 3. Clean and display
            clean_text = response.text.replace('```json', '').replace('```', '')
            st.json(json.loads(clean_text))
            
            # 4. Clean up
            client.files.delete(name=temp_file.name)
            
        except Exception as e:
            st.error(f"Error: {e}")
