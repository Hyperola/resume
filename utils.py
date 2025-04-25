import pdfminer.high_level
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define a shared set of known skills (expand this list as needed)
predefined_skills = {
    "python", "java", "machine learning", "deep learning", "nlp", "sql",
    "flask", "django", "react", "node", "express", "docker", "aws",
    "git", "github", "html", "css", "javascript", "api", "graphql",
    "postgresql", "mongodb", "fastapi", "linux"
}

# Extract raw text from a PDF file
def extract_text_from_pdf(pdf_path):
    return pdfminer.high_level.extract_text(pdf_path)

# Extract relevant skills from resume text
def extract_skills(text):
    doc = nlp(text.lower())
    return list({token.text for token in doc if token.text in predefined_skills})

# Extract relevant skills from job description text
def process_job_description(job_desc):
    doc = nlp(job_desc.lower())
    return list({token.text for token in doc if token.text in predefined_skills})

# Compare extracted resume skills with job description skills and calculate match %
def match_resume_with_job(resume_text, job_desc):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(process_job_description(job_desc))
    if not job_skills:
        return 0.0
    return len(resume_skills & job_skills) / len(job_skills) * 100
