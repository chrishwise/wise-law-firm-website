from Lib.is_safe_url import is_safe_url

import flask
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<p>Login</p>"


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.admin'))


@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p>"


@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    # If there is an existing Admin in the db, display admin sign-in page
    if Admin.query.first():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = Admin.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)

                    next_url = request.args.get('next')
                    # is_safe_url should check if the url is safe for redirects.
                    # See http://flask.pocoo.org/snippets/62/ for an example.
                    #if not is_safe_url(next_url):
                     #   return flask.abort(400)

                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
        return render_template("admin.html")
    # Else, display admin sign-up page
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = Admin.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                new_admin = Admin(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_admin)
                db.session.commit()
                flash('Admin account created!', category='success')
                return redirect(url_for('views.admin'))
        return render_template("admin_signup.html")




