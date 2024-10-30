from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash

from . import db, mail
from .forms import AdminSignUpForm, AdminLoginForm
from .models import Admin

auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.admin_login'))


@auth.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm(request.form)
    if request.method == 'POST':
        # Get data from form
        email = form.email.data
        password = form.password.data
        # Retrieve admin object from database with matching email
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            # Need method to retrieve hardcoded admin password (not hashed) in addition to normal encrypted passwords
            if check_password_hash(admin.password, password) or admin.password == password:
                flash('Logged in!', category='success')
                admin.authenticated = True
                login_user(admin, remember=True)
                return redirect(url_for('views.admin_portal'))
            else:
                print(admin.password)
                print(check_password_hash(admin.password, password))
                flash('Incorrect password, try again.', category='error')
                return redirect(request.url)
        else:
            flash('Email does not exist.', category='error')
            return redirect(request.url)
    return render_template("admin.html", form=form, logged_in=current_user.is_authenticated)


@auth.route('/admin-signup', methods=['GET', 'POST'])
@login_required
def admin_signup():
    form = AdminSignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        new_admin = Admin(email=email, password=password, first_name=first_name,
                          receives_notifications=form.notifications.data)
        db.session.add(new_admin)
        db.session.commit()
        # Send email to notify the new admin of their log in credentials.
        body = "A new admin account for WLF's website was just created using your email address." \
               "\n\nAdmin First Name: " + form.first_name.data + \
               "\nAdmin Email: " + form.email.data + \
               "\nAdmin Password: " + form.password.data + \
               "\n\nThe password, as well as the other settings can be changed from the admin portal."
        title = "Wise Law Firm Website: Your Admin Account Has Been Created"
        msg = Message(subject=title,
                      body=body,
                      recipients=[form.email.data])
        msg.html = render_template("email.html", email=msg)
        mail.send(msg)
        flash("Admin account created! Notification email sent", category='success')
        return redirect(url_for('views.admin_portal'))
    return render_template('admin_signup.html', form=form,
                           logged_in=current_user.is_authenticated)




