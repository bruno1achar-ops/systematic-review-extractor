import streamlit as st
from google import genai
import json

st.title("Systematic Review Data Extractor")

# The client uses the GEMINI_API_KEY from Streamlit Secrets
client = genai.Client()

user_fields = st.text_area("Fields to extract (e.g., Author, Year, Population):", "Author, Year, Population")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # 1. Upload to Google's servers
            temp_file = client.files.upload(
                file=uploaded_file,
                config={"mime_type": "application/pdf"}
            )
            
            # 2. Define the extraction instructions
            prompt = f"""
            Analyze the uploaded PDF. 
            Extract the following fields: {user_fields}.
            Return the output in valid JSON format only, with no extra text.
            """
            
            # 3. Call the model
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[temp_file, prompt]
            )
            
            # 4. Clean and display
            result = response.text.replace('```json', '').replace('```', '')
            st.json(json.loads(result))
            
            # 5. Cleanup
            client.files.delete(name=temp_file.name)
            
        except Exception as e:
            st.error(f"Extraction Error: {e}")
