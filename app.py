from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
import os
import spacy
import sys
from spacy.cli import download
import magic
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, extract_skills, process_job_description, match_resume_with_job, detect_language
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from spellchecker import SpellChecker
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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

spell_checker = SpellChecker()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    analyses = db.relationship('Analysis', backref='user', lazy=True)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skills = db.Column(db.String(1000))
    job_skills = db.Column(db.String(1000))
    match_score = db.Column(db.Float)
    language = db.Column(db.String(50))
    missing_skills = db.Column(db.String(1000))
    typos = db.Column(db.String(1000))
    suggestions = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Registration successful'})
        except:
            return jsonify({'success': False, 'message': 'Email already exists'}), 400

    return jsonify({'success': False, 'message': 'Method not allowed'}), 405

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
                os.remove(filepath)

    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_desc")
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    if not job_desc:
        return jsonify({'success': False, 'message': 'Job description is required'}), 400

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        try:
            mime = magic.Magic()
            file_type = mime.from_file(filepath)

            if "pdf" in file_type.lower():
                resume_text = extract_text_from_pdf(filepath)
            elif "word" in file_type.lower():
                resume_text = extract_text_from_docx(filepath)
            elif "text" in file_type.lower():
                resume_text = extract_text_from_txt(filepath)
            else:
                return jsonify({'success': False, 'message': 'Unsupported file type'}), 400

            language = detect_language(resume_text)
            resume_skills = extract_skills(resume_text)
            job_skills = process_job_description(job_desc)
            match_score = match_resume_with_job(resume_text, job_desc)

            # Check for typos
            words = resume_text.split()
            typos = []
            for word in words:
                if word.isalpha() and not spell_checker.known([word]):
                    typos.append(word)

            # Find missing skills
            missing_skills = [skill for skill in job_skills if skill not in resume_skills]

            # Suggest enhancements
            suggestions = []
            if len(resume_text.split()) < 200:
                suggestions.append("Your resume is too short. Consider adding more details about your experience and skills.")
            if match_score < 50:
                suggestions.append("Your resume has a low match score. Consider tailoring it more closely to the job description.")
            for skill in missing_skills[:3]:
                suggestions.append(f"Add '{skill}' to your resume to better match the job requirements.")

            # Store results in database (for simplicity, assuming user_id=1)
            analysis = Analysis(
                user_id=1,  # Placeholder; implement proper user authentication later
                skills=','.join(resume_skills),
                job_skills=','.join(job_skills),
                match_score=match_score,
                language=language,
                missing_skills=','.join(missing_skills),
                typos=','.join(typos),
                suggestions=','.join(suggestions)
            )
            db.session.add(analysis)
            db.session.commit()

            # Store latest analysis in temporary storage for immediate retrieval
            analysis_results = {
                'skills': resume_skills,
                'job_skills': job_skills,
                'matchScore': round(match_score, 2),
                'language': language,
                'missing_skills': missing_skills,
                'typos': typos,
                'suggestions': suggestions
            }

            return jsonify({'success': True, 'message': 'Upload successful', 'analysis': analysis_results})

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error processing file: {str(e)}'}), 500

        finally:
            os.remove(filepath)

@app.route("/results", methods=["GET"])
def get_results():
    # Fetch the latest analysis for the user (placeholder user_id=1)
    analysis = Analysis.query.filter_by(user_id=1).order_by(Analysis.timestamp.desc()).first()
    if not analysis:
        return jsonify({
            'skills': [],
            'job_skills': [],
            'matchScore': 0,
            'language': 'Unknown',
            'missing_skills': [],
            'typos': [],
            'suggestions': []
        })
    return jsonify({
        'skills': analysis.skills.split(','),
        'job_skills': analysis.job_skills.split(','),
        'matchScore': analysis.match_score,
        'language': analysis.language,
        'missing_skills': analysis.missing_skills.split(','),
        'typos': analysis.typos.split(','),
        'suggestions': analysis.suggestions.split(',')
    })

@app.route("/history", methods=["GET"])
def get_history():
    # Fetch all analyses for the user (placeholder user_id=1)
    analyses = Analysis.query.filter_by(user_id=1).order_by(Analysis.timestamp.desc()).all()
    history = []
    for analysis in analyses:
        history.append({
            'skills': analysis.skills.split(','),
            'job_skills': analysis.job_skills.split(','),
            'matchScore': analysis.match_score,
            'language': analysis.language,
            'missing_skills': analysis.missing_skills.split(','),
            'typos': analysis.typos.split(','),
            'suggestions': analysis.suggestions.split(',')
        })
    return jsonify(history)

@app.route("/export_pdf", methods=["GET"])
def export_pdf():
    # Fetch the latest analysis for the user (placeholder user_id=1)
    analysis = Analysis.query.filter_by(user_id=1).order_by(Analysis.timestamp.desc()).first()
    if not analysis:
        return jsonify({'success': False, 'message': 'No analysis found'}), 404

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    # Write the analysis to the PDF
    p.setFont("Helvetica", 16)
    p.drawString(50, y, "Novaspire Resume Analysis")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, "Skills Detected in Resume:")
    y -= 20
    for skill in analysis.skills.split(','):
        p.drawString(70, y, f"- {skill}")
        y -= 15
    y -= 10

    p.drawString(50, y, "Job Description Skills:")
    y -= 20
    for skill in analysis.job_skills.split(','):
        p.drawString(70, y, f"- {skill}")
        y -= 15
    y -= 10

    p.drawString(50, y, f"Match Score: {analysis.match_score}%")
    y -= 20

    p.drawString(50, y, f"Language: {analysis.language}")
    y -= 20

    p.drawString(50, y, "Missing Skills:")
    y -= 20
    for skill in analysis.missing_skills.split(','):
        p.drawString(70, y, f"- {skill}")
        y -= 15
    y -= 10

    p.drawString(50, y, "Typos Detected:")
    y -= 20
    typos = analysis.typos.split(',')
    if typos == ['']:
        p.drawString(70, y, "No typos found")
        y -= 15
    else:
        for typo in typos:
            p.drawString(70, y, f"- {typo}")
            y -= 15
    y -= 10

    p.drawString(50, y, "Enhancement Suggestions:")
    y -= 20
    for suggestion in analysis.suggestions.split(','):
        p.drawString(70, y, f"- {suggestion}")
        y -= 15

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='resume_analysis.pdf', mimetype='application/pdf')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = "0.0.0.0" if os.getenv("RENDER") else "127.0.0.1"
    app.run(host=host, port=port, debug=True)