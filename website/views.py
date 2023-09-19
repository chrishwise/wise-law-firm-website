import datetime
import threading
import os
import boto3
from flask import Blueprint, render_template, abort, request, flash, g, url_for, json
from flask_login import current_user, login_required
from flask_mail import Message
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from . import db, mail
from .forms import ContactForm, ArticleForm, AdminAccountForm, AdminChangePasswordForm, MasterPasswordForm, \
    CreateAttorneyForm
from .models import Article, Admin, Attorney, AttorneyEducation, AttorneyProfessionalLicense, \
AttorneyProfessionalActivity, AttorneyAdmission, AttorneyMembership, AttorneyPublication, AttorneyAreaOfPractice


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
    return render_template('manage-employees.html', logged_in=False, form=form, employees=employees,
                           current_user=current_user)


@views.route('/create-attorney', methods=['GET', 'POST'])
@login_required
def create_attorney():
    form = CreateAttorneyForm(request.form)
    local_placeholder = "../static/images/avatar-placeholder.png"
    if request.method == 'POST' and form.validate():
        name = form.name.data
        title = form.title.data
        email = form.email.data
        phone = form.phone_number.data
        about = form.about.data

        professional_licenses = form.professional_licenses.data
        professional_activities = form.professional_activities.data
        education = form.education.data
        publications = form.publications.data
        areas_of_practice = form.areas_of_practice.data
        admissions = form.admissions.data
        memberships = form.memberships.data

        new_attorney = Attorney(name=name, title=title, email=email, phone=phone, about=about)
        db.session.add(new_attorney)
        db.session.commit()

        list_of_licenses = professional_licenses.split('\n')
        for l in list_of_licenses:
            new_license = AttorneyProfessionalLicense(title=l, attorney=new_attorney)
            db.session.add(new_license)
        db.session.commit()

        list_of_activities = professional_activities.split('\n')
        for l in list_of_activities:
            new_activity = AttorneyProfessionalActivity(title=l, attorney=new_attorney)
            db.session.add(new_activity)
        db.session.commit()

        list_of_education = education.split('\n')
        for e in list_of_education:
            list_of_fields = e.split(', ')
            degree = list_of_fields[0]
            school = list_of_fields[1]
            year = list_of_fields[2]
            if len(list_of_fields > 3):
                accolades = list_of_fields[3]
            else:
                accolades = ''
            new_attorney_education = AttorneyEducation(degree=degree, school=school, year=year, accolades=accolades,
                                                       attorney=new_attorney)
            print(new_attorney_education.to_string())
            db.session.add(new_attorney_education)
        db.session.commit()

        list_of_publications = publications.split('\n')
        for l in list_of_publications:
            list_of_fields = l.split(', ')
            title = list_of_fields[0]
            details = list_of_fields[1]
            publication = list_of_fields[2]
            year = list_of_fields[3]
            new_publication = AttorneyPublication(title=title, details=details, publication=publication, year=year,
                                                  attorney=new_attorney)
            db.session.add(new_publication)
        db.session.commit()

        list_of_aop = areas_of_practice.split('\n')
        for l in list_of_aop:
            new_aop = AttorneyAreaOfPractice(name=l, attorney=new_attorney)
            db.session.add(new_aop)
        db.session.commit()

        list_of_admissions = admissions.split('\n')
        for l in list_of_admissions:
            list_of_fields = l.split(', ')
            court = list_of_fields[0]
            year = list_of_fields[1]
            new_admission = AttorneyAdmission(court=court, year=year, attorney=new_attorney)
            db.session.add(new_admission)
        db.session.commit()

        list_of_memberships = memberships.split('\n')
        for l in list_of_memberships:
            new_membership = AttorneyMembership(name=l, attorney=new_attorney)
            db.session.add(new_membership)
        db.session.commit()

        flash('New Attorney Has Been Created', category='success')
        return redirect(url_for('views.manage_employees'))
    return render_template('create-attorney.html', logged_in=False, form=form, picture_url=local_placeholder,
                           current_user=current_user)


@views.route('/edit-attorney/<int:aId>', methods=['GET', 'POST'])
@login_required
def edit_attorney(aId):
    form = CreateAttorneyForm(request.form)
    current_attorney = Attorney.query.get(aId)
    if request.method == 'POST' and form.validate():

        db.session.commit()
        flash('Attorney details saved', category='success')
        return redirect(url_for('views.manage_employees'))
    return render_template('edit-attorney.html', logged_in=False, form=form,
                           current_user=current_user, current_attorney=current_attorney)


@views.route('/delete_attorney/<int:aId>')
@login_required
def delete_attorney(aId):
    db.session.delete(Attorney.query.get(aId))
    db.session.commit()
    flash('Attorney was successfully deleted', category='success')
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






boto3_client_lock = threading.Lock()


def create_client():
    '''Uses a threading Lock to prevent multi-threading related errors'''
    with boto3_client_lock:
        return boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))


@views.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = create_client()

    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
