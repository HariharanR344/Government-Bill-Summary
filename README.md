# Government-Bill-Summary

import Required Libraries streamlit → to create the web application pypdf → to read and extract text from PDF files google.generativeai → to generate AI summaries using Gemini

Configure Streamlit Page Sets the page title and layout Displays the app heading and instructions

Take Gemini API Key from User Accepts the Gemini API key securely using a password input Stops the app if the key is not provided Configures Gemini using the given API key

Load Gemini Model Uses the Gemini model (gemini-3-flash-preview) to generate text responses

Upload PDF File Allows the user to upload only PDF files Stores the uploaded government bill for processing

Define Government Bill Keywords Creates keyword and phrase lists related to: Bills Parliament Government Legal and policy terms These are used to validate whether the PDF is a government bill

Validate the PDF Reads the first few pages of the PDF Checks for government-related keywords and mandatory phrases Stops execution if the document is not a valid government bill

Extract Full Text from PDF Extracts text from all pages of the PDF Combines the text into one string for analysis

Create Prompt for Gemini AI Prepares a structured prompt asking Gemini to: Identify bill title Provide summary Explain objectives List impacts, provisions, risks, and opportunities

Generate AI Summary Sends the prompt and extracted text to Gemini Displays the AI-generated summary on the Streamlit app

Error Handling Uses try-except to catch and display errors safely
