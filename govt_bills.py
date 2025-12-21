import streamlit as st
import pypdf
import google.generativeai as genai


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

# ✅ Supported Gemini model
model = genai.GenerativeModel("models/gemini-3-flash-preview")


# PDF Upload 

uploaded_file = st.file_uploader(
    "📄 Upload Government Bill PDF",
    type=["pdf"]
)


# UPDATED KEYWORDS (Supports Introduced Bills)

government_keywords = [
    # Core Bill Indicators
    "bill",
    "introduce a bill",
    "leave to introduce",
    "i introduce the bill",
    "motion was adopted",

    # Parliamentary Terms
    "parliament",
    "lok sabha",
    "rajya sabha",
    "hon. chairperson",
    "hon chairperson",
    "house",

    # Government & Authority
    "government",
    "minister",
    "ministry",
    "authority",
    "regulatory",
    "oversight",

    # Legal & Policy Language
    "regulate",
    "prohibit",
    "public interest",
    "legal framework",
    "national-level",
    "jurisdiction",

    # Digital / Sectoral
    "online gaming",
    "digital technologies",
    "computer resource",
    "mobile device",
    "internet",
    "financial systems",
    "public order",
    "public health",
    "security and sovereignty"
]


# UPDATED MANDATORY PHRASES (Flexible)

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

       
        # VALIDATION STEP (IMPROVED & REALISTIC)
       
        check_text = ""
        for i in range(min(3, total_pages)):
            text = reader.pages[i].extract_text()
            if text:
                check_text += text.lower()

        keyword_hits = sum(1 for word in government_keywords if word in check_text)
        mandatory_hit = any(phrase in check_text for phrase in mandatory_phrases)

        if keyword_hits < 3 and not mandatory_hit:
            st.error("❌ This PDF does NOT appear to be a Government Bill.")
            st.stop()

        st.success("✅ Valid Government Bill detected.")

        
        # Extract Full Text
       
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

        if not full_text.strip():
            st.error("Failed to extract text from the PDF.")
            st.stop()

        st.info("📄 Full text extracted successfully.")

     
        # Prompt for Gemini
       
        prompt = f"""
You are a legal and public policy expert.

Analyze the following Government Bill and provide:

1. Title of the Bill
2. Simple Summary (easy for common people)
3. Objective of the Bill
4. Industry-wise Impact
5. Key Provisions
6. Risks and Opportunities

Bill Content:
{full_text}
"""

        if st.button("🔍 Generate Summary"):
            with st.spinner("Generating summary using Gemini AI..."):
                response = model.generate_content(prompt)

                st.subheader("📑 AI Generated Summary")
                st.write(response.text)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
