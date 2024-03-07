import datetime
import threading
import os
import time

import boto3
from flask import Blueprint, render_template, abort, request, flash, g, url_for, json, jsonify
from flask_login import current_user, login_required
from flask_mail import Message
from flask_sqlalchemy.session import Session
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from . import db, mail
from .forms import ContactForm, ArticleForm, AdminAccountForm, AdminChangePasswordForm, MasterPasswordForm, \
    CreateAttorneyForm, RespondEmailForm
from .models import Article, Admin, Attorney, AttorneyEducation, AttorneyProfessionalLicense, \
    AttorneyProfessionalActivity, AttorneyAdmission, AttorneyMembership, AttorneyPublication, AttorneyAreaOfPractice, \
    Contact, ContactResponse

views = Blueprint('views', __name__)
session = Session(db)


@views.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@views.route('/firm-overview')
def firm_overview():
    return render_template("firm-overview.html", logged_in=current_user.is_authenticated)


@views.route('/our-team')
def our_team():
    attorneys = Attorney.query.all()
    return render_template("our-team.html", attorneys=attorneys, logged_in=current_user.is_authenticated)


@views.route('/employee/<int:id>', methods=['GET'])
def employee(id):
    employee = Attorney.query.get(id)
    print(employee.professional_licenses)
    print(employee.areas_of_practice)
    print(employee.memberships)
    print(employee.education)
    return render_template("employee-template.html", employee=employee, logged_in=current_user.is_authenticated)


@views.route('david-wise')
def david_wise():
    return render_template("david-wise.html", logged_in=current_user.is_authenticated)


@views.route('joe-langone')
def joe_langone():
    return render_template("joe-langone.html", logged_in=current_user.is_authenticated)


@views.route('david-reese')
def david_reese():
    return render_template("david-reese.html", logged_in=current_user.is_authenticated)


@views.route('william-evans')
def evan_williams():
    return render_template("william-evans.html", logged_in=current_user.is_authenticated)


@views.route('dylan-graham')
def dylan_graham():
    return render_template("dylan-graham.html", logged_in=current_user.is_authenticated)


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
def articles(id=0):
    articles = Article.query.all()
    if articles:
        if id == 0:
            article = get_first_article()
        else:
            article = Article.query.get_or_404(id)
    else:
        print("there are no current articles")
        no_articles = Article(title="There are no new articles posted at the moment", text="Come back soon!")
        db.session.add(no_articles)
        db.session.commit()
        article = no_articles
    return render_template("articles.html", articles=articles, article=article, logged_in=current_user.is_authenticated)


@views.route('/admin-portal/manage-articles/<int:id>', methods=['GET', 'POST'])
@login_required
def manage_articles(id=0):
    articles = Article.query.all()
    if articles:
        if id == 0:
            article = get_first_article()
        else:
            article = Article.query.get_or_404(id)
    else:
        print("there are no current articles")
        no_articles = Article(title="There are no new articles posted at the moment", text="Come back soon!")
        db.session.add(no_articles)
        db.session.commit()
        article = no_articles
    return render_template('manage-articles.html', logged_in=False, article=article, articles=articles)


def get_first_article():
    return Article.query.order_by(desc(Article.date)).first()


@views.route('/create', methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = Article(title=form.title.data, text=form.text.data, date=datetime.date.today(),
                          published_date=form.publishing_date.data, url=form.url.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('views.articles', id=article.id))
    return render_template("new-article.html", form=form, logged_in=current_user.is_authenticated)


@views.route('/delete-article/<int:id>', methods=['GET', 'POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash("Article was successfully deleted!", category='success')
    return redirect(url_for('views.articles', id=0))


@views.route('/edit-article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    form = ArticleForm(request.form)
    article = Article.query.get_or_404(id)
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
        form.text.data = article.text       # Using the the render field value parameter in the html template didn't work so I set the value here
    return render_template('edit-article.html', form=form, article=article, logged_in=current_user.is_authenticated)


@views.route('/careers')
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
        admins_receiving_notifications = Admin.query.filter_by(receives_notifications=True).all()
        recipient_list = []
        for admin in admins_receiving_notifications:
            recipient_list.append(admin.email)
        print('recipient list: ', recipient_list)
        msg = Message(subject=title,
                      body=body,
                      sender="no-reply-wiselawfirm@outlook.com",
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
    return render_template("contact-us.html", form=form, logged_in=current_user.is_authenticated)


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
    return render_template('admin-portal.html', logged_in=False, form=form,
                           current_user=current_user)


@views.route('/admin-portal/manage-employees', methods=['GET', 'POST'])
@login_required
def manage_employees():
    form = None
    employees = Attorney.query.all()
    return render_template('manage-employees.html', logged_in=False, form=form, attorneys=employees,
                           current_user=current_user)


@views.route('/create-employee', methods=['GET', 'POST'])
@login_required
def create_employee():
    form = CreateAttorneyForm(request.form)
    header = "Create Employee"
    button = "Create Employee"
    local_placeholder = "../static/images/avatar-placeholder.png"
    if request.method == 'POST':
        attorney_id = form.new_attorney_id.data
        print(f"attorney_id is: {attorney_id}")
        new_attorney = session.query(Attorney).get(attorney_id)
        if form.validate():
            name = form.name.data
            title = form.title.data
            email = form.email.data
            phone = form.phone_number.data
            about = form.about.data

            new_attorney.update(name=name, title=title, email=email, phone=phone, about=about)
            session.commit()
            session.close()
            flash('New Attorney Has Been Created', category='success')
            return redirect(url_for('views.manage_employees'))
        else:
            flash('Failed to Create New Attorney', category='error')
    else:       # request != 'POST'
        if not session.is_active:
            session.begin()
        new_attorney = Attorney()
        session.add(new_attorney)
        session.flush()  # Don't want to commit but need the attorney.id
        form.new_attorney_id.data = new_attorney.id
        print(f"new_attorney's id is: {new_attorney.id}")
    return render_template('create-attorney.html', logged_in=False, form=form, picture_url=local_placeholder,
                           current_user=current_user, current_attorney=new_attorney, header=header, button=button)


@views.route('/add_license', methods=['GET', 'POST'])
@login_required
def add_license():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        title = json_data[1]['title']
        new_license = AttorneyProfessionalLicense(title=title, attorney=attorney)
        session.add(new_license)
        session.flush()
        results = {'title': title,
                   'licenseId': new_license.id}
        return jsonify(results)


@views.route('/edit_license', methods=['GET', 'POST'])
@login_required
def edit_license():
    if request.method == 'POST':
        json_data = request.get_json()
        license_id = int(json_data[0]['id'])
        new_title = json_data[1]['newTitle']
        license = AttorneyProfessionalLicense.query.get(license_id)
        attorney_id = license.attorney_id
        license.title = new_title
        db.session.commit()
        flash('Professional license was successfully saved', category='success')
        results = [{'attorneyId': attorney_id}, {'updatedLicense': license}]
        return jsonify(results)


@views.route('/delete_license', methods=['POST'])
@login_required
def delete_license():
    json_data = request.get_json()
    license_id = json_data[0]['licenseId']
    license = session.query(AttorneyProfessionalLicense).get(license_id)
    print(f"license to delete: {license}")
    session.delete(license)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        title = json_data[1]['title']
        new_activity = AttorneyProfessionalActivity(title=title, attorney=attorney)
        session.add(new_activity)
        session.flush()
        results = {'title': title,
                   'activityId': new_activity.id}
        return jsonify(results)


@views.route('/edit_activity', methods=['GET', 'POST'])
@login_required
def edit_activity():
    if request.method == 'POST':
        json_data = request.get_json()
        activity_id = int(json_data[0]['activityId'])
        new_title = json_data[1]['newTitle']
        activity = AttorneyProfessionalActivity.query.get(activity_id)
        attorney_id = activity.attorney_id
        activity.title = new_title
        session.commit()
        results = [{'attorneyId': attorney_id}, {'activityTitle': activity.title}]
        return jsonify(results)


@views.route('/delete_activity', methods=['POST'])
@login_required
def delete_activity():
    json_data = request.get_json()
    activity_id = json_data[0]['activityId']
    print(f"activity_id: {activity_id}")
    activity = session.query(AttorneyProfessionalActivity).get(activity_id)
    print(f"activity: {activity}")
    session.delete(activity)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/add_education', methods=['GET', 'POST'])
@login_required
def add_education():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(AttorneyEducation).get(attorney_id)
        education = AttorneyEducation(degree=json_data[1]['degree'], school=json_data[2]['school'],
                                      year=json_data[3]['year'], accolades=json_data[4]['accolades'],
                                      attorney=attorney)
        session.add(education)
        session.flush()
        results = {'toString': education.to_string(),
                   'educationId': education.id}
        return jsonify(results)


@views.route('/edit_education', methods=['GET', 'POST'])
@login_required
def edit_education():
    if request.method == 'POST':
        json_data = request.get_json()
        education_id = int(json_data[0]['educationId'])
        education = AttorneyEducation.query.get(education_id)
        education.degree = json_data[1]['degree']
        education.school = json_data[2]['school']
        education.year = json_data[3]['year']
        education.accolades = json_data[4]['accolades']
        session.commit()
        results = [{'toString': education.to_string()},
                   {'educationId': education_id}]
        return jsonify(results)


@views.route('/delete_education', methods=['POST'])
@login_required
def delete_education():
    json_data = request.get_json()
    education_id = json_data[0]['educationId']
    print(f"education_id: {education_id}")
    education = session.query(AttorneyEducation).get(education_id)
    print(f"education: {education}")
    session.delete(education)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/add_publication', methods=['POST'])
@login_required
def add_publication():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        title = json_data[1]['title']
        details = json_data[2]['details']
        publication = json_data[3]['publication']
        year = json_data[4]['year']
        new_publication = AttorneyPublication(title=title, details=details, publication=publication, year=year,
                                              attorney=attorney)
        session.add(new_publication)
        session.flush()
        results = {'toString': new_publication.to_string(),
                   'publicationId': new_publication.id}
        return jsonify(results)


@views.route('/edit_publication', methods=['GET', 'POST'])
@login_required
def edit_publication():
    if request.method == 'POST':
        json_data = request.get_json()
        publication_id = int(json_data[0]['publicationId'])
        publication = AttorneyPublication.query.get(publication_id)
        publication.title = json_data[1]['title']
        publication.details = json_data[2]['details']
        publication.year = json_data[3]['year']
        publication.publication = json_data[4]['publication']
        session.commit()
        results = [{'toString': publication.to_string()},
                   {'publicationId': publication_id}]
        return jsonify(results)


@views.route('/delete_publication', methods=['POST'])
@login_required
def delete_publication():
    json_data = request.get_json()
    publication_id = json_data[0]['publicationId']
    print(f"publication_id: {publication_id}")
    publication = session.query(AttorneyPublication).get(publication_id)
    print(f"publication: {publication}")
    session.delete(publication)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/add_aop', methods=['POST'])
@login_required
def add_aop():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        name = json_data[1]['name']
        new_aop = AttorneyAreaOfPractice(name=name, attorney=attorney)
        session.add(new_aop)
        session.flush()
        results = {'toString': new_aop.to_string(),
                   'aopId': new_aop.id}
        return jsonify(results)


@views.route('/edit_aop', methods=['GET', 'POST'])
@login_required
def edit_aop():
    if request.method == 'POST':
        json_data = request.get_json()
        aop_id = int(json_data[0]['aopId'])
        new_title = json_data[1]['newName']
        aop = AttorneyAreaOfPractice.query.get(aop_id)
        attorney_id = aop.attorney_id
        aop.title = new_title
        session.commit()
        results = [{'attorneyId': attorney_id}, {'aopTitle': aop.title}]
        return jsonify(results)


@views.route('/delete_aop', methods=['POST'])
@login_required
def delete_aop():
    json_data = request.get_json()
    aop_id = json_data[0]['aopId']
    print(f"aop_id: {aop_id}")
    aop = session.query(AttorneyAreaOfPractice).get(aop_id)
    print(f"aop: {aop}")
    session.delete(aop)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/add_admission', methods=['POST'])
@login_required
def add_admission():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        court = json_data[1]['court']
        year = json_data[2]['year']
        new_admission = AttorneyAdmission(court=court, year=year, attorney=attorney)
        session.add(new_admission)
        session.flush()
        results = {'toString': new_admission.to_string(),
                   'admissionId': new_admission.id}
        return jsonify(results)


@views.route('/edit_admission', methods=['GET', 'POST'])
@login_required
def edit_admission():
    if request.method == 'POST':
        json_data = request.get_json()
        admission_id = int(json_data[0]['admissionId'])
        new_court = json_data[1]['court']
        new_year = json_data[2]['year']
        admission = AttorneyAdmission.query.get(admission_id)
        attorney_id = admission.attorney_id
        admission.court = new_court
        admission.year = new_year
        session.commit()
        results = [{'attorneyId': attorney_id}, {'toString': admission.to_string()}]
        return jsonify(results)


@views.route('/delete_admission', methods=['POST'])
@login_required
def delete_admission():
    json_data = request.get_json()
    admission_id = json_data[0]['admissionId']
    print(f"admission_id: {admission_id}")
    admission = session.query(AttorneyAdmission).get(admission_id)
    print(f"admission: {admission}")
    session.delete(admission)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/add_membership', methods=['POST'])
@login_required
def add_membership():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        name = json_data[1]['name']
        new_membership = AttorneyMembership(name=name, attorney=attorney)
        session.add(new_membership)
        session.flush()
        results = {'toString': new_membership.to_string(),
                   'membershipId': new_membership.id}
        return jsonify(results)


@views.route('/edit_membership', methods=['GET', 'POST'])
@login_required
def edit_membership():
    if request.method == 'POST':
        json_data = request.get_json()
        membership_id = int(json_data[0]['membershipId'])
        new_name = json_data[1]['name']
        membership = AttorneyMembership.query.get(membership_id)
        attorney_id = membership.attorney_id
        membership.name = new_name
        session.flush()
        results = [{'attorneyId': attorney_id}, {'toString': membership.to_string()}]
        return jsonify(results)


@views.route('/delete_membership', methods=['POST'])
@login_required
def delete_membership():
    json_data = request.get_json()
    print(json_data)
    membership_id = json_data[0]['membershipId']
    print(f"membership_id: {membership_id}")
    membership = session.query(AttorneyMembership).get(membership_id)
    print(f"membership: {membership}")
    session.delete(membership)
    session.flush()
    return jsonify({'true': 'true'})


@views.route('/edit-employee/<int:eId>', methods=['GET', 'POST'])
@login_required
def edit_employee(eId):
    form = CreateAttorneyForm(request.form)
    header = "Edit Employee"
    button = "Save Changes"
    current_attorney = Attorney.query.get(eId)
    form.name.data = current_attorney.name
    form.email.data = current_attorney.email
    form.title.data = current_attorney.title
    form.phone_number.data = current_attorney.phone_number
    form.about.data = current_attorney.about
    form.picture_url.data = current_attorney.picture_url

    if request.method == 'POST' and form.validate():
        current_attorney.name = form.name.data
        current_attorney.title = form.title.data
        current_attorney.email = form.email.data
        current_attorney.phone = form.phone_number.data
        current_attorney.about = form.about.data

        db.session.commit()
        flash('Attorney details saved', category='success')
        return redirect(url_for('views.manage_employees'))
    return render_template('create-attorney.html', logged_in=False, form=form, header=header, button=button,
                           current_user=current_user, current_attorney=current_attorney)


@views.route('/delete_attorney/<int:aId>')
@login_required
def delete_attorney(aId):
    db.session.delete(Attorney.query.get(aId))
    db.session.commit()
    flash('Attorney was successfully deleted', category='success')
    return redirect(url_for('views.manage_employees'))


@views.route('/admin-portal/manage-reviews', methods=['GET', 'POST'])
@login_required
def manage_reviews():
    form = None
    return render_template('manage-reviews.html', logged_in=False, form=form,
                           current_user=current_user)


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
                           logged_in=False, current_user=current_user)


@views.route('/edit-admin/<int:adminId>', methods=['GET', 'POST'])
@login_required
def edit_admin(adminId):
    form = AdminAccountForm(request.form)
    current_admin = Admin.query.get(adminId)
    form.notifications.data = current_admin.receives_notifications
    form.first_name.data = current_admin.first_name
    form.email.data = current_admin.email
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
        new_password = generate_password_hash(form.new_password.data)
        current_user.change_password(new_password)
        db.session.commit()
        flash("Admins password has successfully been changed", category='success')
        return redirect(url_for('views.admin_portal'))
    return render_template('change-password.html', form=form, logged_in=False,
                           current_user=current_user)


@views.route('/contact-submissions', methods=['GET', 'POST'])
@login_required
def contact_submissions():
    contacts = Contact.query.filter_by(archived=False).all()

    # The following is for responding to contact submissions from within the admin portal
    respondForm = RespondEmailForm(request.form)
    if request.method == 'POST' and respondForm.validate():
        recipients = respondForm.recipients.data
        # This ensures that recipients is a list
        if type(recipients) is not list:
            recipients = recipients.split()

        # get contact by id from hidden input in form
        contactId = request.form.get('contactId')
        contact = Contact.query.get(contactId)
        contact.responded = True
        # create and add contact response to database
        contact_response = ContactResponse(message=respondForm.message.data, contact=contact)
        db.session.add(contact_response)
        db.session.commit()

        email = Message(subject="Response to your Wise Law Firm form submission",
                        body=respondForm.message.data,
                        recipients=recipients)
        email.html = render_template('email-response.html', email=email)
        mail.send(email)
        flash('Response email has been sent', category='success')
        return redirect(url_for('views.contact_submissions'))
    return render_template('contact-submissions.html', logged_in=False, form=respondForm, contacts=contacts)


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
                           logged_in=False,
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
    return render_template('contact-archive.html', logged_in=False, contacts=archived_contacts,
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
