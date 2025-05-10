import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth = Blueprint('auth', __name__)

DB_PATH = 'Hjemmeside/Database/credentials.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        company = request.form.get('company')
        password = request.form['password']

        db = get_db()
        try:
            db.execute(
                'INSERT INTO CREDENTIALS (EMAIL, FIRSTNAME, LASTNAME, COMPANY, PASSWORD)'
                'VALUES (?, ?, ?, ?, ?)',
                (email, firstname, lastname, company, password)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash('That email is already registered.')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        pw = request.form['password']

        db = get_db()
        user = db.execute(
            "SELECT FIRSTNAME, PASSWORD FROM CREDENTIALS WHERE EMAIL = ?",
            (email,)
        ).fetchone()
        db.close()

        if user and user['FIRSTNAME'] == firstname and user['PASSWORD'] == pw:
            session['user_email'] = email
            return redirect(url_for('routes.home'))
        
        flash('Invalid email, firstname or password.')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('routes.home'))

@auth.route('/download')
def download():
    return render_template('download.html')

@auth.route('/about_us')
def about_us():
    return render_template('about_us.html')

@auth.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')