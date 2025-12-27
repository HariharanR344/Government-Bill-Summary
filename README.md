# Government-Bill-Summary

The Government Bill PDF Analyzer is an end-to-end NLP and Generative AI–based application developed to validate and analyze Indian Government Bill documents. The project demonstrates a complete text analytics workflow, from PDF text extraction and NLP preprocessing to structured policy analysis using Google Gemini AI, deployed through a Streamlit web application following industry-standard practices.

Data Collection
Government Bill documents are collected in the form of PDF files uploaded by the user through the Streamlit interface. These PDFs typically originate from official sources such as Lok Sabha and Rajya Sabha portals and contain legal and policy-related content.

Document Validation
Before analysis, the uploaded PDF is validated to ensure it is a genuine Government Bill. The system scans the initial pages of the document for government-specific keywords and mandatory legal phrases commonly found in official bills. If the required conditions are not met, the document is rejected, preventing invalid or unrelated PDFs from being processed.

PDF Text Extraction
Once validated, the complete textual content of the PDF is extracted using PyPDF. The extracted text from all pages is combined into a single corpus for further processing.

NLP Preprocessing
The extracted text undergoes multiple NLP preprocessing steps to improve AI understanding:
Conversion to lowercase for uniformity
Removal of URLs and HTML tags
Removal of punctuation and special characters
Tokenization of text into individual words
Stopword removal to eliminate non-informative words
Spell correction using a spell-checking module
These steps ensure the text is clean, standardized, and suitable for language model analysis.

Prompt
A structured prompt is designed to instruct the AI model to act as a legal and public policy expert. The prompt clearly specifies the required outputs, including the bill title, simplified summary, objectives, industry-wise impact, short-, medium-, and long-term impact assessment, positives, negatives, risks, and opportunities.

Model Integration
The preprocessed bill content is passed to Google Gemini AI (gemini-3-flash-preview), which generates an in-depth and structured analysis based on the provided prompt.

Streamlit Application
The entire workflow is deployed using Streamlit, providing an interactive interface for:
Secure API key input
PDF upload
Validation status display
AI-generated policy analysis
This enables real-time, user-friendly interaction for both technical and non-technical users.
