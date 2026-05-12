from flask import Flask, render_template, request, redirect, session, flash
import os
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from utils.parser import extract_text_from_resume
from utils.analyzer import extract_skills
from utils.preprocess import preprocess_text
from utils.predict import predict_category

from utils.ats_score import (
    calculate_ats_score,
    missing_skills,
    keyword_match
)

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def home():
    return redirect('/login')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form['email']
        new_password = request.form['new_password']

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        # hash new password
        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            "UPDATE users SET password=? WHERE email=?",
            (hashed_password, email)
        )

        conn.commit()
        conn.close()

        flash('Password reset successful!')
        return redirect('/login')

    return render_template('forgot_password.html')



@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username, email, password) VALUES(?,?,?)",
                (username, email, hashed_password)
            )

            conn.commit()
            flash("Registration Successful! Please login.")
            return redirect('/login')

        except:
            flash("Email already exists")

        finally:
            conn.close()

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        
        if user and check_password_hash(user[3], password):

            session['user'] = user[1]   # username
            session['email'] = user[2]   # email

            
            return redirect('/dashboard')

        else:
            flash("Invalid Email or Password")

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    
    return redirect('/login')



@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history WHERE user_email=?",
        (session['email'],)
    )

    history = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', history=history)


@app.route('/upload', methods=['POST'])
def upload_resume():

    if 'user' not in session:
        return redirect('/login')

    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

   
    extracted_text = extract_text_from_resume(filepath)

    if not extracted_text:
        return "Could not extract text from resume"

    job_description = request.form.get('job_description', '')

    processed_tokens = preprocess_text(extracted_text)
    skills = extract_skills(extracted_text)

    ats_score = calculate_ats_score(extracted_text, job_description)
    missing = missing_skills(extracted_text, job_description)
    match_percentage = keyword_match(extracted_text, job_description)

    predicted_category = predict_category(extracted_text)

   
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO history(user_email, ats_score, category)
        VALUES(?,?,?)
        ''',
        (session['email'], ats_score, predicted_category)
    )

    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        text=extracted_text,
        filename=filename,
        skills=skills,
        tokens=processed_tokens,
        ats_score=ats_score,
        missing=missing,
        match_percentage=match_percentage,
        predicted_category=predicted_category
    )



if __name__ == "__main__":
    app.run(debug=True)