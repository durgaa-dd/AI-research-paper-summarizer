import streamlit as st
from PyPDF2 import PdfReader
import requests

# -----------------------------------
# OpenRouter API Key
# -----------------------------------
API_KEY = "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"

# -----------------------------------
# Streamlit UI
# -----------------------------------
st.title("📘 ScholarBot")

st.write("AI Research Paper Summarizer")

# -----------------------------------
# Upload PDF
# -----------------------------------
uploaded_file = st.file_uploader(
    "Upload Research Paper PDF",
    type="pdf"
)

# -----------------------------------
# Read PDF
# -----------------------------------
if uploaded_file is not None:

    st.success("PDF Uploaded Successfully ✅")

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    # Extract text from PDF
    for page in pdf_reader.pages:

        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text

    # -----------------------------------
    # Show Extracted Text
    # -----------------------------------
    st.subheader("📄 Extracted Text")

    st.text_area(
        "Paper Content",
        text[:3000],
        height=300
    )

    # -----------------------------------
    # Generate Summary
    # -----------------------------------
    if st.button("Generate Summary"):

        with st.spinner("Generating AI Summary..."):

            try:

                prompt = f"""
                Summarize this research paper in simple language:

                {text[:3000]}
                """

                response = requests.post(

                    url="https://openrouter.ai/api/v1/chat/completions",

                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },

                    json={
                        "model": "openai/gpt-3.5-turbo",

                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }
                )

                result = response.json()

                if "choices" in result:

                    summary = result["choices"][0]["message"]["content"]

                    st.subheader("🤖 AI Summary")

                    st.write(summary)

                else:

                    st.error("API Error")

                    st.write(result)

            except Exception as e:

                st.error(f"Error: {e}")