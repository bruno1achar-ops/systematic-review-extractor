import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="Extractor", layout="wide")
st.title("Systematic Review Data Extractor")

# 1. Initialize API Key
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. Setup Model
model = genai.GenerativeModel('gemini-1.5-flash')

user_fields = st.text_area("Fields (comma separated):", "Author, Year, Population, Intervention, Outcome")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing..."):
        try:
            # Upload file to Gemini API
            pdf_data = uploaded_file.getvalue()
            
            # Using the File API
            myfile = genai.upload_file(uploaded_file, mime_type="application/pdf")
            
            prompt = f"Extract {user_fields} from this PDF. Return ONLY valid JSON."
            
            # Generate response
            response = model.generate_content([myfile, prompt])
            
            # Clean up the JSON string (removing markdown code blocks)
            json_text = response.text.replace('```json', '').replace('```', '')
            data = json.loads(json_text)
            
            st.success("Extraction Complete!")
            st.json(data)
            
        except Exception as e:
            st.error(f"CRITICAL ERROR: {str(e)}")
