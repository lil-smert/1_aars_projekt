import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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

        hashed_password = generate_password_hash(password)

        try:
            db.execute(
                'INSERT INTO CREDENTIALS '
                '(EMAIL, FIRSTNAME, LASTNAME, COMPANY, USERNAME, PASSWORD)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (email, firstname, lastname, company, username, hashed_password)
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
        #Tjek at brugeren findes og at passwordet er korrekt, fra hash
        if user and check_password_hash(user['PASSWORD'], pw):
            session['user_email'] = user['EMAIL']
            return redirect(url_for('routes.home'))
        
        flash('Invalid email, firstname or password.')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('routes.home'))

@auth.route('/api/login', methods=['POST']) #Skal læses op på, men det er en API i JSON, spillet sender et POST request til URL'en, i JSON format
def api_login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"status": "error", "message": "Invalid request."}), 400
    username = data['username'].strip()
    pw = data['password']
    

    db = get_db()
    user = db.execute(
        "SELECT USERNAME, PASSWORD FROM CREDENTIALS WHERE USERNAME = ?",
        (username,)
    ).fetchone()
    db.close()
    

    #Tjek at brugeren findes og at passwordet er korrekt, fra hash
    if user and check_password_hash(user['PASSWORD'], pw): #Tjekker om
        return jsonify({"status": "success", "username": user['USERNAME']})
      
    return jsonify({"status": "error", "message": "Invalid username or password."}), 401

@auth.route('/api/submit', methods=['POST'])
def receive_data():
    data = request.get_json()
    username = data.get('username')
    level1 = data.get('level_1')
    level2 = data.get('level_2')
    level3 = data.get('level_3')
    level4 = data.get('level_4')
    db = get_db()
    user = db.execute("""INSERT OR REPLACE INTO GAME_DATA (USERNAME, LEVEL1, LEVEL2, LEVEL3, LEVEL4) VALUES (?, ?, ?, ?, ?)""",
        (username, level1, level2, level3, level4)
    )
    db.commit()
    db.close()
    return jsonify({"status": "success", "message": "Data received successfully."}), 200

@auth.route('/api/get_data', methods=['GET'])
def send_data():
    username = request.args.get('username') #modtager brugernavn
    db = get_db()
    data = db.execute("SELECT LEVEL1, LEVEL2, LEVEL3, LEVEL4 FROM GAME_DATA WHERE USERNAME = ?", (username,)).fetchone()
    db.close()
    if data:
        return jsonify(
            {
                "level_1": data['LEVEL1'],
                "level_2": data['LEVEL2'],
                "level_3": data['LEVEL3'],
                "level_4": data['LEVEL4'],
                "status": "success"
            }
        )
    else:
        return jsonify({"status": "error", "message": "No data found."}), 404

@auth.route('/download')
def download():
    return render_template('download.html')

@auth.route('/about_us')
def about_us():
    return render_template('about_us.html')

@auth.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')