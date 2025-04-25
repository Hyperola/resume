from flask import Flask, render_template, request
import os
import spacy
import sys
from spacy.cli import download

from utils import extract_text_from_pdf, extract_skills, process_job_description, match_resume_with_job

app = Flask(__name__)

# Ensure the spaCy model is available
MODEL_NAME = "en_core_web_sm"
try:
    nlp = spacy.load(MODEL_NAME)
    print(f"Successfully loaded {MODEL_NAME}")
except OSError:
    print(f"Model {MODEL_NAME} not found. Attempting to download...")
    try:
        download(MODEL_NAME)
        nlp = spacy.load(MODEL_NAME)
        print(f"Successfully downloaded and loaded {MODEL_NAME}")
    except Exception as e:
        print(f"Failed to download {MODEL_NAME}: {e}")
        sys.exit(1)

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
    # Get the port from the environment variable (Render sets this), default to 5000 for local dev
    port = int(os.getenv("PORT", 5000))
    # Bind to 0.0.0.0 for Render, 127.0.0.1 for local dev
    host = "0.0.0.0" if os.getenv("RENDER") else "127.0.0.1"
    app.run(host=host, port=port, debug=True)