import datetime
import os
import threading
from typing import List, Any

import boto3
from flask import Blueprint, render_template, request, flash, url_for, json, send_from_directory
from flask import current_app as app
from flask_login import current_user, login_required
from flask_mail import Message
from flask_sqlalchemy.session import Session
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from . import db, mail
from .forms import ContactForm, ArticleForm, AdminAccountForm, AdminChangePasswordForm, MasterPasswordForm, \
    RespondEmailForm, ReviewForm, PracticeAreaForm
from .models import Article, Admin, Attorney, Contact, ContactResponse, Review, PracticeArea

views = Blueprint('views', __name__)
session = Session(db)


@views.route('/sitemap.xml')
@views.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@views.route('/')
def home():
    articles = db.session.query(Article).order_by(desc(Article.date)).all()
    return render_template("index.html", articles=articles, public_view=True)


@views.route('/firm-overview')
def firm_overview():
    # practice_areas = PracticeArea.query.all()                              # Don't need this because context processor
    return render_template("firm-overview.html", public_view=True)  # practice_areas=practice_areas ^


@views.route('/our-team')
def our_team():
    attorneys = Attorney.query.all()
    return render_template("our-team.html", attorneys=attorneys, public_view=True)


@views.route('/employee/<int:id>', methods=['GET'])
def employee(id):
    employee = Attorney.query.get(id)
    return render_template("employee-template.html", employee=employee, public_view=True)


#
# @views.route('/practice-areas', methods=['GET'])
# def practice_areas():
#     practice_areas = db.session.query(PracticeArea).order_by(PracticeArea.id).all()
#     return render_template('practice-areas.html', practice_areas=practice_areas, public_view=True)
#

@views.route('/practice-area/<int:id>')
def practice_area(id):
    practice_area = PracticeArea.query.get_or_404(id, 'No Practice Area exists in the database '
                                                      'with an id of {id}'.format(id=id))
    return render_template('practice-area.html', practice_area=practice_area, public_view=True)


@views.route('/reviews')
def reviews():
    reviews = db.session.query(Review).order_by(Review.date).all()
    return render_template("reviews.html", reviews=reviews, public_view=True)


def get_first_article():
    return Article.query.order_by(desc(Article.date)).first()


@views.route('/articles/<int:id>')
def articles(id=1):
    articles = Article.query.all()
    if articles:
        article = Article.query.get_or_404(id)
    else:
        print("there are no current articles")
        no_articles = Article(title="There are no new articles posted at the moment", text="Come back soon!", date=datetime.date.today())
        db.session.add(no_articles)
        db.session.commit()
        article = no_articles
    return render_template("articles.html", articles=articles, article=article, public_view=True)


@views.route('/careers')
def careers():
    return render_template("careers.html", public_view=True)


@views.route('/maps')
def maps():
    return render_template("maps.html", public_view=True)


@views.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        body = "Contact Email:   " + form.email.data + "\r\nMessage:   \r\n\r\n" + form.message.data
        title = "WLF website: New Message from " + request.form.get('name')
        admins_receiving_notifications = Admin.query.filter_by(receives_notifications=True).all()
        recipient_list = []
        for admin in admins_receiving_notifications:
            recipient_list.append(admin.email)
        print('recipient list: ', recipient_list)
        msg = Message(subject=title,
                      body=body,
                      recipients=recipient_list)
        msg.html = render_template("email.html", email=msg)
        mail.send(msg)
        flash("Message was successfully sent!", category='success')

        # create Contact object and add it to the database
        contact_us_submission = Contact(name=form.name.data,
                                        email=form.email.data,
                                        message=form.message.data,
                                        date_time=datetime.datetime.now(),
                                        responded=False)
        db.session.add(contact_us_submission)
        db.session.commit()

        return redirect(url_for('views.home'))
    return render_template("contact-us.html", form=form, public_view=True)


@views.route('/admin-portal', methods=['GET', 'POST'])
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
    else:
        form.notifications.data = current_user.receives_notifications

    return render_template('admin-portal.html', public_view=False, form=form,
                           current_user=current_user)


# I moved all the view functions related to new employees/attorneys to employees.py
@views.route('/admin-portal/manage-employees', methods=['GET', 'POST'])
@login_required
def manage_employees():
    form = None
    employees = Attorney.query.order_by(Attorney.id).all()
    return render_template('manage-employees.html', public_view=False, form=form, attorneys=employees,
                           current_user=current_user)


@views.route('/manage_practice_areas', methods=['GET', 'POST'])
@login_required
def manage_practice_areas():
    # I don't need to pass practice_areas to the render_template function because of context processors
    return render_template('manage-practice-areas.html', public_view=False,
                           current_user=current_user)


@views.route('/edit_practice_area/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_practice_area(id):
    form = PracticeAreaForm(request.form)
    practice_area = db.session.query(PracticeArea).get(id)
    title = 'Edit Practice Area'
    button = 'Save'
    if request.method == 'POST' and form.validate():
        practice_area.name = form.title.data
        practice_area.description = form.description.data
        practice_area.full_text = form.full_text.data
        practice_area.icon_url = form.icon_url.data
        practice_area.picture_url = form.picture_url.data
        print(practice_area.picture_url, form.picture_url.data, practice_area.icon_url, form.icon_url.data)
        db.session.commit()
        flash('Practice Area was successfully updated', category='success')
        return redirect(url_for('views.manage_practice_areas'))
    else:
        form.title.data = practice_area.name
        form.description.data = practice_area.description
        form.full_text.data = practice_area.full_text
        form.picture_url.data = practice_area.picture_url
        form.icon_url.data = practice_area.icon_url
        print(form, form.picture_url.data, form.icon_url.data)
    return render_template("new-practice-area.html", form=form, public_view=False, title=title, button=button)


@views.route('/new_practice_area', methods=['GET', 'POST'])
@login_required
def new_practice_area():
    form = PracticeAreaForm(request.form)
    title = 'New Practice Area'
    button = 'Submit'
    if request.method == 'POST' and form.validate():
        practice_area = PracticeArea(name=form.title.data, description=form.description.data, full_text=form.full_text.data,
                                     icon_url=form.icon_url.data, picture_url=form.picture_url.data)
        db.session.add(practice_area)
        db.session.commit()
        flash('Practice Area was successfully created', category='success')
        return redirect(url_for('views.manage_practice_areas'))
    return render_template("new-practice-area.html", form=form, public_view=False, title=title, button=button)


@views.route('/delete-practice-area/<int:id>', methods=['GET'])
@login_required
def delete_practice_area(id):
    db.session.delete(PracticeArea.query.get_or_404(id))
    db.session.commit()
    flash('Practice Area was successfully deleted', category='success')
    return redirect(url_for('views.manage_practice_areas'))



@views.route('/admin-portal/manage-reviews', methods=['GET'])
@login_required
def manage_reviews():
    reviews = db.session.query(Review).all()
    return render_template('manage-reviews.html', public_view=False, reviews=reviews,
                           current_user=current_user)


@views.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = ReviewForm(request.form)
    header = "New Review"
    if request.method == 'POST' and form.validate():
        review = Review(content=form.content.data, date=datetime.date.today(), author=form.author.data)
        db.session.add(review)
        db.session.commit()
        flash('Review was successfully created', category='success')
        return redirect(url_for('views.manage_reviews'))
    return render_template("new-review.html", form=form, header=header, public_view=False)


@views.route('/edit_review/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_review(id):
    form = ReviewForm(request.form)
    header = "Edit Review"
    review = db.session.query(Review).get(id)
    if request.method == 'POST' and form.validate():
        review.content = form.content.data
        review.author = form.author.data
        db.session.commit()
        flash('Review was successfully updated', category='success')
        return redirect(url_for('views.manage_reviews'))
    else:
        form.content.data = review.content
        form.author.data = review.author
    return render_template("new-review.html", form=form, public_view=False, header=header)


@views.route('/delete_review/<int:id>', methods=['GET'])
@login_required
def delete_review(id):
    db.session.delete(Review.query.get(id))
    db.session.commit()
    flash('Review was successfully deleted', category='success')
    return redirect(url_for('views.manage_reviews'))


@views.route('/admin-portal/manage-articles/<int:id>', methods=['GET', 'POST'])
@login_required
def manage_articles(id=0):
    articles: List[Any] = Article.query.all()
    if articles:
        if id == 0:
            article = get_first_article()
        else:
            article = Article.query.get_or_404(id)
    else:
        print("there are no current articles")
        no_articles = Article(title="There are no new articles posted at the moment", text="Come back soon!",
                              date=datetime.date.today())
        db.session.add(no_articles)
        db.session.commit()
        articles = [no_articles]
        article = articles[0]
        print('articles: ', articles)
    return render_template('manage-articles.html', article=article, articles=articles, public_view=False)


@views.route('/new-article', methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm(request.form)
    title = 'New Article'
    if request.method == 'POST' and form.validate():
        article = Article(title=form.title.data, text=form.text.data, date=datetime.date.today(),
                          published_date=form.publishing_date.data, url=form.url.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('views.articles', id=article.id))
    return render_template("new-article.html", form=form, title=title, public_view=False)


@views.route('/edit-article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    form = ArticleForm(request.form)
    article = Article.query.get_or_404(id)
    title = "Edit Article"
    if request.method == 'POST' and form.validate():
        article.title = form.title.data
        article.published_date = form.publishing_date.data
        article.date = form.date_created.data
        article.url = form.url.data
        article.text = form.text.data
        db.session.commit()
        flash("Article has been updated successfully!", category='success')
        return redirect(url_for('views.manage_articles', id=id))
    elif request.method == 'GET':
        form.text.data = article.text
        # Using the render field value parameter in the html template didn't work, so I set the value here
    return render_template('new-article.html', form=form, article=article, title=title, public_view=False)


@views.route('/delete-article/<int:id>', methods=['GET', 'POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash("Article was successfully deleted!", category='success')
    return redirect(url_for('views.articles', id=0))


@views.route('/admin-portal/manage-admins', methods=['GET', 'POST'])
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
                           public_view=False, current_user=current_user)


@views.route('/edit-admin/<int:adminId>', methods=['GET', 'POST'])
@login_required
def edit_admin(adminId):
    form = AdminAccountForm(request.form)
    current_admin = Admin.query.get(adminId)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        email = form.email.data
        wants_notifications = form.notifications.data
        current_admin.replace_name(first_name)
        if email != current_admin.email:
            current_admin.replace_email(email)
        current_admin.sets_notifications(wants_notifications)
        print(f"current admin: {current_admin.to_string()}")
        db.session.commit()
        flash('Admin details saved', category='success')
        return redirect(url_for('views.manage_admins'))
    else:
        form.notifications.data = current_admin.receives_notifications
        form.first_name.data = current_admin.first_name
        form.email.data = current_admin.email
    return render_template('edit-admin-account.html', public_view=False, form=form,
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
        new_password = generate_password_hash(form.new_password.data)
        current_user.change_password(new_password)
        db.session.commit()
        flash("Admins password has successfully been changed", category='success')
        return redirect(url_for('views.admin_portal'))
    return render_template('change-password.html', form=form, public_view=False,
                           current_user=current_user)


@views.route('/contact-submissions', methods=['GET', 'POST'])
@login_required
def contact_submissions():
    contacts = Contact.query.filter_by(archived=False).order_by(Contact.date_time.desc()).all()

    # The following is for responding to contact submissions from within the admin portal
    respond_form = RespondEmailForm(request.form)
    if request.method == 'POST' and respond_form.validate():
        recipients = respond_form.recipients.data
        # This ensures that recipients is a list
        if type(recipients) is not list:
            recipients = recipients.split()

        # get contact by id from hidden input in form
        contact_id = request.form.get('contactId')
        contact = Contact.query.get(contact_id)
        contact.responded = True
        # create and add contact response to database
        contact_response = ContactResponse(message=respond_form.message.data, contact=contact)
        db.session.add(contact_response)
        db.session.commit()

        email = Message(subject="Response to your Wise Law Firm form submission",
                        body=respond_form.message.data,
                        recipients=recipients)
        email.html = render_template('email-response.html', email=email)
        mail.send(email)
        flash('Response email has been sent', category='success')
        return redirect(url_for('views.contact_submissions'))
    return render_template('contact-submissions.html', public_view=False, form=respond_form, contacts=contacts)


@views.route('/toggle-responded/<int:id>', methods=['GET'])
@login_required
def toggle_responded(id):
    contact = Contact.query.get(id)
    if contact.responded:
        contact.responded = False
    else:
        contact.responded = True
    db.session.commit()
    flash("The responded field has been updated.", category='success')
    return redirect(url_for('views.contact_submissions'))


@views.route('/toggle-archive/<int:id>', methods=['GET'])
@login_required
def toggle_archive(id):
    contact = Contact.query.get(id)
    # If already archived, set as false to negate this
    if contact.archived:
        contact.archived = False
        flash("Contact Submission has been unarchived.", category='success')
    # Otherwise set as true to archive this submission
    else:
        contact.archived = True
        flash("Contact Submission has been archived.", category='success')
    db.session.commit()
    return redirect(url_for('views.contact_submissions'))


@views.route('/delete-contact/<int:id>', methods=['GET'])
@login_required
def delete_contact(id):
    to_delete = Contact.query.get(id)
    db.session.delete(to_delete)
    flash("Contact Submission has been deleted", category='success')
    db.session.commit()
    return redirect(url_for('views.contact_submissions'))


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
                           public_view=False,
                           current_user=current_user)


@views.route('/manage-admins/toggle-master', methods=['GET'])
def toggle_master():
    current_user.remove_master_clearance()
    db.session.commit()
    flash('Master clearance has been turned off for the logged-in admin', category='success')
    return redirect(url_for('views.manage_admins'))


@views.route('/contact-archive', methods=['GET', 'POST'])
def contact_archive():
    archived_contacts = Contact.query.filter_by(archived=True).all()
    print(archived_contacts)
    return render_template('contact-archive.html', public_view=False, contacts=archived_contacts,
                           current_user=current_user)


# This is for uploading pictures to Amazon S3 Bucket


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

    json_output = json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
    print("when signing s3 request: ", json_output)

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
