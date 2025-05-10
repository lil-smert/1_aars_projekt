from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth = Blueprint('auth', __name__)

#Definer credentials
USERS = {
    'simon-nikolajsen@live.dk': {'firstname': 'Simon', 'password': '12345'},
}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        pw = request.form.get('password')

        user = USERS.get(email)
        if user and user['firstname'] == firstname and user['password'] == pw:
            session['user_email'] = email
            return redirect(url_for('routes.home'))
        flash('Invalid email, First name or password')

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