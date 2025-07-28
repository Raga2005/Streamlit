import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF text extraction

# Set up page
st.set_page_config(page_title="📄 Resume Analyzer with Gemini", layout="centered")
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume PDF and get improvement suggestions powered by **Gemini AI**.")

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyD-Yat3AG1c-JvWlNQoyQcGfXILglNiMD8"  # 🔐 Replace this with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Upload PDF resume
uploaded_file = st.file_uploader("📤 Upload your Resume (PDF only)", type=["pdf"])

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Analyze resume with Gemini
def analyze_resume(resume_text):
    prompt = (
        "You are an expert resume reviewer and career coach.\n\n"
        "Here is a resume:\n\n"
        f"{resume_text}\n\n"
        "Please provide constructive and actionable feedback to improve this resume, including:\n"
        "- Formatting and structure\n"
        "- Grammar and clarity\n"
        "- Skills and keyword usage\n"
        "- ATS compatibility\n"
        "- Any other suggestions for improvement\n\n"
        "Respond in detailed bullet points."
    )
    response = model.generate_content(prompt)
    return response.text

# Main logic
if uploaded_file is not None:
    with st.spinner("⏳ Extracting and analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if len(resume_text.strip()) == 0:
            st.error("❌ Could not extract any text from the PDF. Try a different file.")
        else:
            suggestions = analyze_resume(resume_text)
            st.success("✅ Analysis complete!")
            st.subheader("📌 Suggestions to Improve Your Resume:")
            st.markdown(suggestions)
else:
    st.info("Please upload your resume to get started.")
