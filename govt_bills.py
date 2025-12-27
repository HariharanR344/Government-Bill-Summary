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

st.title("📜 Government Bill PDF Analyzer")
st.write(
    "Upload a Government Bill PDF to validate and summarize it using Gemini AI."
)


# Gemini API Key Input

api_key = st.text_input(
    "🔑 Enter your Google Gemini API Key",
    type="password"
)

if not api_key:
    st.warning("Please enter your Gemini API key to proceed.")
    st.stop()

genai.configure(api_key=api_key)

# Gemini Model
model = genai.GenerativeModel("models/gemini-3-flash-preview")


# NLP PREPROCESSING FUNCTION

def preprocess_text(text):
    spell = SpellChecker()

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove punctuation & special characters
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Tokenization
    tokens = text.split()

    # Stopword removal
    stopwords = {
        "the", "is", "and", "a", "an", "of", "to", "in", "for", "on",
        "with", "by", "this", "that", "it", "as", "are", "be"
    }
    tokens = [word for word in tokens if word not in stopwords]

    # Spell checking
    corrected_tokens = []
    for word in tokens:
        corrected = spell.correction(word)
        corrected_tokens.append(corrected if corrected else word)

    # Reconstruct clean text
    clean_text = " ".join(corrected_tokens)

    return clean_text


# PDF Upload

uploaded_file = st.file_uploader(
    "📄 Upload Government Bill PDF",
    type=["pdf"]
)


# Government Bill Keywords

government_keywords = [
    "bill", "introduce a bill", "leave to introduce",
    "i introduce the bill", "motion was adopted",
    "parliament", "lok sabha", "rajya sabha",
    "government", "minister", "ministry",
    "regulate", "public interest", "be it enacted"
]


# Mandatory Legal Phrases

mandatory_phrases = [
    "introduce a bill",
    "leave be granted to introduce",
    "i introduce the bill",
    "motion was adopted",
    "statement of objects and reasons",
    "be it enacted"
]


# Processing Logic

if uploaded_file:
    try:
        reader = pypdf.PdfReader(uploaded_file)
        total_pages = len(reader.pages)

        if total_pages == 0:
            st.error("The uploaded PDF has no pages.")
            st.stop()

        st.success(f"📄 Total Pages Detected: {total_pages}")

        #Validation Step 
        check_text = ""

        for i in range(min(3, total_pages)):
            page_text = reader.pages[i].extract_text()
            if page_text:
                check_text += page_text.lower()

        keyword_hits = sum(
            1 for word in government_keywords if word in check_text
        )

        mandatory_hit = any(
            phrase in check_text for phrase in mandatory_phrases
        )

        if keyword_hits < 3 and not mandatory_hit:
            st.error("❌ This PDF does NOT appear to be a Government Bill.")
            st.stop()

        st.success("✅ Valid Government Bill detected.")

        #Extract Full Text
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

        if not full_text.strip():
            st.error("Failed to extract text from the PDF.")
            st.stop()

        st.info("📄 Full text extracted successfully.")

        #NLP Preprocessing
        processed_text = preprocess_text(full_text)
        st.success("🧹 NLP preprocessing completed.")

        #Gemini Prompt
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
{processed_text}
"""

        #Generate Summary
        if st.button("🔍 Generate Summary"):
            with st.spinner("Generating summary using Gemini AI..."):
                response = model.generate_content(prompt)

            st.subheader("📑 AI Generated Summary")
            st.write(response.text)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
