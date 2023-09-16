import datetime

from flask import Blueprint, render_template, abort, request, flash, g, url_for
from flask_login import current_user, login_required
from flask_mail import Message
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from . import db, mail
from .forms import ContactForm, ArticleForm, AdminAccountForm, AdminChangePasswordForm, MasterPasswordForm, \
    NewEmployeeForm
from .models import Article, Admin, Attorney

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@views.route('/firm-overview')
def firm_overview():
    return render_template("firm-overview.html", logged_in=current_user.is_authenticated)


@views.route('/our-team')
def our_team():
    return render_template("our-team.html", logged_in=current_user.is_authenticated)


@views.route('david-wise')
def david_wise():
    return render_template("david-wise.html", logged_in=current_user.is_authenticated)


@views.route('joe-langone')
def joe_langone():
    return render_template("joe-langone.html", logged_in=current_user.is_authenticated)


@views.route('pat-donahue')
def pat_donahue():
    return render_template("pat-donahue.html", logged_in=current_user.is_authenticated)


@views.route('david-reese')
def david_reese():
    return render_template("david-reese.html", logged_in=current_user.is_authenticated)


@views.route('/class-actions')
def class_actions():
    return render_template("class-actions.html", logged_in=current_user.is_authenticated)


@views.route('/construction-law')
def construction_law():
    return render_template("construction-law.html", logged_in=current_user.is_authenticated)


@views.route('/construction-litigation')
def construction_litigation():
    return render_template("construction-litigation.html", logged_in=current_user.is_authenticated)


@views.route('/construction-defect-litigation')
def construction_defect_litigation():
    return render_template("construction-defect-litigation.html", logged_in=current_user.is_authenticated)


@views.route('/wrongful-death')
def wrongful_death():
    return render_template("wrongful-death.html", logged_in=current_user.is_authenticated)


@views.route('/commercial-and-business')
def commercial_and_business():
    return render_template("commercial-and-business.html", logged_in=current_user.is_authenticated)


@views.route('/mold-and-environmental')
def mold_and_environmental():
    return render_template("mold-and-environmental.html", logged_in=current_user.is_authenticated)


@views.route('/government-contracts')
def government_contracts():
    return render_template("government-contracts.html", logged_in=current_user.is_authenticated)


@views.route('/insurance-coverage')
def insurance_coverage():
    return render_template("insurance-coverage.html", logged_in=current_user.is_authenticated)


@views.route('/reviews')
def reviews():
    return render_template("reviews.html", logged_in=current_user.is_authenticated)


@views.route('/articles/<int:id>')
@views.route('/articles/<int:id>/<admin_editable>')
@views.route('/articles/<admin_editable>')
def articles(admin_editable=False, id=0):
    articles = Article.query.all()
    if articles:
        if id == 0:
            article = get_first_article()
        else:
            article = Article.query.get_or_404(id)
    else:
        print("there are no current articles")
        no_articles = Article(title="There is no new articles posted at the moment", text="Come back soon!")
        db.session.add(no_articles)
        db.session.commit()
        article = no_articles
    return render_template("articles.html", articles=articles, article=article, logged_in=False,
                           admin_editable=admin_editable)


def get_first_article():
    return Article.query.order_by(desc(Article.date)).first()


@views.route('/create', methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = Article(title=form.title.data, text=form.text.data, date=form.date_created,
                          published_date=form.publishing_date.data, user_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('views.articles', id=article.id))
    return render_template("new-article.html", form=form, logged_in=False)


@views.route('/delete-article/<int:id>', methods=['GET', 'POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash("Article was successfully deleted!")
    return redirect(url_for('views.articles'))


@views.route('/edit-article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    form = ArticleForm(request.form)
    article = Article.query.get_or_404(id)
    if request.method == 'POST' and form.validate():
        article.title = form.title.data
        article.text = form.text.data
        article.date = form.date_added.data
        article.publishing_date = form.publishing_date.data
        db.session.commit()
        return redirect(url_for('views.articles', id=id))
    elif request.method == 'GET':
        form.text.data = article.text
    return render_template('edit-article.html', form=form, article=article, logged_in=False)


@views.route('careers')
def careers():
    return render_template("careers.html", logged_in=current_user.is_authenticated)


@views.route('/maps')
def maps():
    return render_template("maps.html", logged_in=current_user.is_authenticated)


@views.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        body = "Contact Email: " + form.email.data + "\n\nMessage: \n\n" + form.message.data
        title = "WLF website: New Message from " + request.form.get('name')
        msg = Message(subject=title,
                      body=body,
                      sender="no-reply-wiselawfirm@outlook.com",
                      recipients=['chris@wisertech.pro', 'ltanous@wiselaw.pro', 'cwise@wiselaw.pro', 'dwise@wiselaw.pro', 'jwise@wiselaw.pro', 'mhumphreys@wiselaw.pro', 'jlangone@wiselaw.pro'])
        msg.html = render_template("email.html", email=msg)
        mail.send(msg)
        flash("Message was successfully sent!")
        return redirect(url_for('views.home'))
    return render_template("contact-us.html", form=form, logged_in=current_user.is_authenticated)


@views.route('admin-portal/', methods=['GET', 'POST'])
@login_required
def admin_portal():
    form = AdminAccountForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        email = form.email.data
        wants_notifications = form.notifications.data
        current_user.replace_name(first_name)
        current_user.replace_email(email)
        current_user.sets_notifications(wants_notifications)
        db.session.commit()
        flash('Admin details saved', category='success')
    return render_template('admin-portal.html', logged_in=False, form=form,
                           current_user=current_user)


@views.route('admin-portal/manage-employees', methods=['GET', 'POST'])
@login_required
def manage_employees():
    form = None
    employees = Attorney.query.all()
    return render_template('manage-employees.html', logged_in=current_user.is_authenticated, form=form, employees=employees,
                           current_user=current_user)


@views.route('admin-portal/manage-employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = NewEmployeeForm(request.form)
    return render_template('add-employee.html', logged_in=current_user.is_authenticated, form=form,
                           current_user=current_user)


@views.route('/delete/<int:eId>')
@login_required
def delete_employee(eId):
    db.session.delete(Admin.query.get(eId))
    db.session.commit()
    flash('Employee was successfully deleted', category='success')
    return redirect(url_for('views.manage_employees'))


@views.route('admin-portal/manage-reviews', methods=['GET', 'POST'])
@login_required
def manage_reviews():
    form = None
    return render_template('manage-reviews.html', logged_in=False, form=form,
                           current_user=current_user)


@views.route('admin-portal/manage-articles', methods=['GET', 'POST'])
@login_required
def manage_articles():
    form = None
    return render_template('manage-articles.html', logged_in=False, form=form,
                           current_user=current_user)


@views.route('admin-portal/manage-admins', methods=['GET', 'POST'])
@login_required
def manage_admins():
    admins = Admin.query.all()
    if current_user.has_master_clearance():
        editable = True
    else:
        editable = False
    notified = Admin.query.filter_by(receives_notifications=True).all()
    notified_admins = ''
    for admin in notified:
        notified_admins += admin.email
        notified_admins += ', '
    if len(notified_admins) > 3:
        notified_admins = notified_admins.removesuffix(', ')

    return render_template('manage-admins.html', admins=admins, editable=editable, notified_admins=notified_admins,
                           logged_in=False, current_user=current_user)


@views.route('/edit-admin/<int:adminId>', methods=['GET', 'POST'])
@login_required
def edit_admin(adminId):
    form = AdminAccountForm(request.form)
    current_admin = Admin.query.get(adminId)
    form.notifications.data = current_admin.receives_notifications
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        email = form.email.data
        wants_notifications = form.notifications.data
        current_admin.replace_name(first_name)
        if email != current_admin.email:
            current_admin.replace_email(email)
        current_admin.sets_notifications(wants_notifications)
        db.session.commit()
        flash('Admin details saved', category='success')
        return redirect(url_for('views.manage_admins'))
    return render_template('edit-admin-account.html', logged_in=current_user.is_authenticated, form=form,
                           current_user=current_user, current_admin=current_admin)


@views.route('/delete/<int:adminId>')
@login_required
def delete_admin(adminId):
    db.session.delete(Admin.query.get(adminId))
    db.session.commit()
    flash('Admin was successfully deleted', category='success')
    return redirect(url_for('views.manage_admins'))


@views.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = AdminChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        new_password = generate_password_hash(form.new_password.data, method='scrypt')
        current_user.change_password(new_password)
        db.session.commit()
        flash("Admins password has successfully been changed", category='success')
        return redirect(url_for('views.admin_account'))
    return render_template('change-password.html', form=form, logged_in=False,
                           current_user=current_user)


@views.route('/contact-submissions', methods=['GET'])
@login_required
def contact_submissions():
    return render_template('contact-submissions.html', logged_in=False, contact_submissions=contact_submissions)


@views.route('/master_password', methods=['GET', 'POST'])
@login_required
def master_privileges():
    form = MasterPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.set_master_clearance()
        db.session.commit()
        flash('Master Privileges Granted', category='success')
        return redirect(url_for('views.manage_admins'))
    return render_template('master-privileges.html', form=form,
                           logged_in=current_user.is_authenticated,
                           current_user=current_user)


@views.route('/manage-admins/toggle-master', methods=['GET'])
def toggle_master():
    current_user.remove_master_clearance()
    db.session.commit()
    flash('Master clearance has been turned off for the logged-in admin', category='success')
    return redirect(url_for('views.manage_admins'))