from unicodedata import name
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)

# if /login is requested login.html is rendered, and if a post request happens then form data is captured and verified


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if post request is made do the following
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        logindata = request.form
        print("New login", logindata)

        user = User.query.filter_by(email=email).first()
        # if the hashed password (hashed using wekzeug.security) matches that of the user login the user
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template('login.html', user=current_user)


# the "/" route is the home page
@auth.route('/', methods=['GET', 'POST'])
def newsletter():
    if request.method == 'POST':
        newsletteremail = request.form.get('newsletteremail')
        newsletterdata = request.form
        print("New newsletter info", newsletterdata)
        flash('Thanks for joining our Newsletter', category='success')
    return render_template('home.html', user=current_user)


# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Signup


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        agree = request.form.get('agree')
        bday = request.form.get('trip-start')
        the_date = datetime.strptime(bday, '%Y-%m-%d')

        signupdata = request.form
        print("New Signup Data", signupdata)

        print("NEW SIGNUP!!!! Details: ", email,
              name, password1, password2, agree, the_date)
        user = User.query.filter_by(email=email).first()

        if user:
            flash('User already registered with this email', category='error')

        if len(email) < 4:
            flash('Invalid email', category='error')
        elif len(name) < 2:
            flash('Name must be at least 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif agree == None:
            flash('Please agree to the Terms of Service', category='error')
            print("terms box not ticked")
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
