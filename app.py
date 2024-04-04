from dotenv import load_dotenv
from PIL import Image
import os
import google.generativeai as genai
import streamlit as st
import PyPDF2 

#Loading the API_KEY
load_dotenv()

#Loading the model
model=genai.GenerativeModel("gemini-pro")

def get_gemini_response(input, content):
    response=model.generate_content([input, content])
    return response

def PDF_extractor(pdf):
    read_pdf = PyPDF2.PdfReader(pdf)
    page = read_pdf.pages[0]
    page_content = page.extract_text()
    return page_content

# Streamlit Setup

st.set_page_config(page_title="CV Information Scrapper")

st.header("CV Information Scrapper")
uploaded_file=st.file_uploader("Upload your CV...", type=["pdf"])

    
submit=st.button("Submit")

input_prompt= """

You act as a Data Scrawler. Based on the uploaded_file, skim and scan, then find the necessary information to categorize everything in the cv file into a dict format:

For example:

{
    "Full Name": "Quoc",
    "Email":"phamkinhquoc2002@gmail.com"
    "Phone": 29389423,
    "GitHub-Link": "https://github.com/kinhquoc2002,
    "Specialization": ["Data Science", "Project Management"],
    "Experience": {
        "Company": ABCCompany,
        "Position": Data Analyst Intern,
        "Experience": 2 years,
    }
}

If you can't find the necessary information to deduce from the provided image, please input None inside the dict file! 

"""

if submit:
    content=PDF_extractor(uploaded_file)
    response=get_gemini_response(input_prompt,content)
    st.write(response.text)