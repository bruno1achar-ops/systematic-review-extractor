# Replace the upload block in app.py with this:
if uploaded_file and st.button("Extract Data"):
    with st.spinner("Processing document..."):
        try:
            # 1. Read bytes
            bytes_data = uploaded_file.getvalue()
            
            # 2. Upload with hard-coded mime_type
            # We explicitly tell the API this is a PDF to avoid the ValueError
            pdf_file = client.files.upload(
                file=bytes_data, 
                config={
                    'display_name': uploaded_file.name, 
                    'mime_type': 'application/pdf'
                }
            )
            
            # 3. Wait for processing (Crucial step for Gemini File API)
            # Sometimes the file needs a second to be ready
            import time
            while pdf_file.state.name == "PROCESSING":
                time.sleep(2)
                pdf_file = client.files.get(name=pdf_file.name)
            
            # 4. Proceed with generation
            prompt = f"Extract the following fields: {schema_list}. Return strictly as JSON."
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[pdf_file, prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            
            # ... (rest of your display code)
