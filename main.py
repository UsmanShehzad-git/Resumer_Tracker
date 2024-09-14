import os
import pdfplumber
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import io

load_dotenv() ##Load all the enironment variables

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Gemini Pro Response
def get_gemini_respsonse(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)

    return response.text



## Prompt Template
input_prompts = '''
Hey Act as like a skilled or very experience ATS(Applocation Tracking System)
with a deep understanding of tech field,software engineering, data science, data analysis
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitve and you should provide the best assistant for
improving your resume. Assign the percentage Matching based on JD and
the missing keyword with high accuracy
resume:{text}\n
description:{jd}\n

I want to response in one single string having the structure
{{"JD Match:"%"\n, "Missing Keywords:[]"\n , "Profile Summary":\n""}}

'''

##Streamlit App
st.set_page_config(page_title="Resume Tracker", initial_sidebar_state="expanded")
st.title("Resume Analyzer")
#st.text("Improve Your Resume using Application Tracking System(ATS)")
st.caption("Improve Your Resume using Application Tracking System(ATS)")

jd = st.text_area("Paste the Job Description")
upload_file = st.file_uploader("Upload Your Resume" , type="pdf", help="please upload the pdf file")

submit = st.button("Submit")
if submit:
    if upload_file is not None:
        #Read the pdf file
        with pdfplumber.open(io.BytesIO(upload_file.getvalue())) as pdf:
         text = ""
         for page in pdf.pages:
             text += page.extract_text()
        #Get the Gemini Response
        response = get_gemini_respsonse(input_prompts)
        st.subheader(response)