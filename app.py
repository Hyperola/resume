from flask import Flask, render_template, request
import os
import spacy  # Import spaCy here
import sys
from spacy.cli import download

from utils import extract_text_from_pdf, extract_skills, process_job_description, match_resume_with_job

app = Flask(__name__)

# Ensure the spaCy model is available
MODEL_NAME = "en_core_web_sm"
try:
    spacy.load(MODEL_NAME)
except OSError:
    print(f"Model {MODEL_NAME} not found. Downloading...")
    download(MODEL_NAME)
    spacy.load(MODEL_NAME)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        if file and job_desc:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            resume_skills = extract_skills(resume_text)
            job_skills = process_job_description(job_desc)
            match_score = match_resume_with_job(resume_text, job_desc)

            return render_template("result.html",
                                   resume_skills=resume_skills,
                                   job_skills=job_skills,
                                   score=round(match_score, 2))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)