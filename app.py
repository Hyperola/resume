from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import spacy
import sys
from spacy.cli import download
import magic

from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, extract_skills, process_job_description, match_resume_with_job, detect_language

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

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

# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except:
            flash("Email already exists. Please choose a different one.", "danger")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        flash("Login failed. Check your email or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            flash("No file uploaded.", "danger")
            return redirect(url_for("index"))

        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        if file and job_desc:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Determine file type
            mime = magic.Magic()
            file_type = mime.from_file(filepath)

            try:
                if "pdf" in file_type.lower():
                    resume_text = extract_text_from_pdf(filepath)
                elif "word" in file_type.lower():
                    resume_text = extract_text_from_docx(filepath)
                elif "text" in file_type.lower():
                    resume_text = extract_text_from_txt(filepath)
                else:
                    flash("Unsupported file type.", "danger")
                    return redirect(url_for("index"))

                # Detect language of the resume
                language = detect_language(resume_text)

                resume_skills = extract_skills(resume_text)
                job_skills = process_job_description(job_desc)
                match_score = match_resume_with_job(resume_text, job_desc)

                return render_template("result.html",
                                       resume_skills=resume_skills,
                                       job_skills=job_skills,
                                       score=round(match_score, 2),
                                       language=language)

            finally:
                os.remove(filepath)  # Clean up the uploaded file

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = "0.0.0.0" if os.getenv("RENDER") else "127.0.0.1"
    app.run(host=host, port=port, debug=True)