import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth = Blueprint('auth', __name__)

DB_PATH = 'Hjemmeside/Database/credentials.db'

#Liste over godkendte firmaer
AUTHORIZED_COMPANIES = {
    "KEA",
    "Frederiksberg Kommune",
    "Gooner Games Inc",
}

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        company = request.form.get('company', "").strip()
        username = request.form['username'].strip()
        password = request.form['password']


        #Hvis firmaet ikke er i listen over godkendte firmaer
        if company not in AUTHORIZED_COMPANIES:
            flash('Sorry, "%s" is not authorized to register for our services.' % company)
            return redirect(url_for('auth.register'))

        db = get_db()

        #Tjek at username er unikt
        if db.execute(
            "SELECT 1 FROM CREDENTIALS WHERE USERNAME = ?",
            (username,)
        ).fetchone():
            flash(f"Username '{username}' is already taken.")
            db.close()
            return redirect(url_for('auth.register'))
        
        try:
            db.execute(
                'INSERT INTO CREDENTIALS '
                '(EMAIL, FIRSTNAME, LASTNAME, COMPANY, USERNAME, PASSWORD)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (email, firstname, lastname, company, username, password)
            )
            db.commit()
        except sqlite3.IntegrityError:
            db.rollback()
            flash('That email is already registered.')
            return redirect(url_for('auth.register'))
        
        finally:
            db.close()
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        pw = request.form['password']

        db = get_db()
        user = db.execute(
            "SELECT EMAIL, PASSWORD FROM CREDENTIALS WHERE USERNAME = ?",
            (username,)
        ).fetchone()
        db.close()

        if user and user['PASSWORD'] == pw:
            session['user_email'] = user['EMAIL']
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