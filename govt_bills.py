import streamlit as st
import pypdf
import google.generativeai as genai
import re
from spellchecker import SpellChecker


# Streamlit Page Configuration

st.set_page_config(
    page_title="Government Bill Analyzer",
    layout="centered"
)

st.title("Government Bill PDF Analyzer")
st.write("Upload a Government Bill PDF to validate and summarize it using Gemini AI.")


# Gemini API Key Input

api_key = st.text_input("Enter your Google Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your Gemini API key to proceed.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-3-flash-preview")



# PDF Upload

uploaded_file = st.file_uploader(
    "📄 Upload Government Bill PDF",
    type=["pdf"]
)



# NLP PREPROCESSING FUNCTION

def preprocess_text(text):
    spell = SpellChecker()

    #Lowercase
    text = text.lower()

    #Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    #Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

   
    #Remove punctuation & special characters
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    #Tokenization
    tokens = text.split()

    #Stopword removal
    stopwords = {
        "the", "is", "and", "a", "an", "of", "to", "in", "for", "on",
        "with", "by", "this", "that", "it", "as", "are", "be"
    }
    tokens = [word for word in tokens if word not in stopwords]

    #Spell checking
    corrected_tokens = []
    for word in tokens:
        corrected = spell.correction(word)
        corrected_tokens.append(corrected if corrected else word)

    #Reconstruct clean text
    clean_text = " ".join(corrected_tokens)

    return clean_text



# Processing Logic

if uploaded_file:
    try:
        reader = pypdf.PdfReader(uploaded_file)
        full_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

        if not full_text.strip():
            st.error("Failed to extract text from PDF.")
            st.stop()

        st.success("PDF text extracted successfully.")

       
        # Apply NLP Preprocessing
       
        clean_text = preprocess_text(full_text)
        st.info("NLP preprocessing completed.")


       
        # Gemini Prompt
       
        prompt = f"""
You are a legal and public policy expert.

Analyze the following Government Bill and provide:
1. Title of the Bill
2. Simple Summary (easy for common people)
3. Objective of the Bill
4. Industry-wise Impact
5. Impact Assessment 
● Short term (0-1 year)
● Medium term (1-5 years)
● Long term (>5 years)
6. Positives and Negatives
7. Risks and Opportunities

Bill Content:
{clean_text}
"""


        if st.button("Generate Summary"):
            with st.spinner("Generating summary using Gemini AI..."):
                response = model.generate_content(prompt)

                st.subheader("AI Generated Summary")
                st.write(response.text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
