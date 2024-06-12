import datetime
import threading
import os
import time
from typing import List, Any

import boto3
from flask import Blueprint, render_template, abort, request, flash, g, url_for, json, jsonify, send_from_directory
from flask_login import current_user, login_required
from flask_mail import Message
from flask_sqlalchemy.session import Session
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from flask import current_app as app

from . import db, mail
from .forms import ContactForm, ArticleForm, AdminAccountForm, AdminChangePasswordForm, MasterPasswordForm, \
    CreateAttorneyForm, RespondEmailForm, ReviewForm, PracticeAreaForm
from .models import Article, Admin, Attorney, AttorneyEducation, AttorneyProfessionalLicense, \
    AttorneyProfessionalActivity, AttorneyAdmission, AttorneyMembership, AttorneyPublication, AttorneyAreaOfPractice, \
    Contact, ContactResponse, Review, PracticeArea
from .views import views

employees = Blueprint('employees', __name__)
session = Session(db)


@employees.route('/create-employee', methods=['GET', 'POST'])
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
            picture_url = request.form.get('picture')
            print(f"picture_url: {picture_url}")
            new_attorney.update(name=name, title=title, email=email, phone=phone, about=about, picture_url=picture_url)
            session.commit()
            session.close()
            flash('New Employee Has Been Created', category='success')
            return redirect(url_for('employees.manage_employees'))
        else:
            flash('Failed to Create New Attorney', category='error')
    else:  # request != 'POST'
        if not session.is_active:
            session.begin()
        new_attorney = Attorney()
        session.add(new_attorney)
        session.flush()  # Don't want to commit but need the attorney.id
        form.new_attorney_id.data = new_attorney.id
        print(f"new_attorney's id is: {new_attorney.id}")
    return render_template('create-attorney.html', public_view=False, form=form, picture_url=local_placeholder,
                           current_user=current_user, current_attorney=new_attorney, header=header, button=button)


@employees.route('/edit-employee/<int:eId>', methods=['GET', 'POST'])
@login_required
def edit_employee(eId):
    print(f'session is active: {session.is_active}')
    if not session.is_active:
        print(f'session began')
        session.begin()
    form = CreateAttorneyForm(request.form)
    header = "Edit Employee"
    button = "Save Changes"
    current_attorney = session.query(Attorney).get(eId)
    print(f'current attorney: {current_attorney}')
    print(f'current attorneys education: {current_attorney.education}')
    educations = db.session.query(AttorneyEducation).all()
    print(f'educations: {educations}')
    if request.method == 'POST':
        current_attorney.name = form.name.data
        current_attorney.title = form.title.data
        current_attorney.email = form.email.data
        current_attorney.phone_number = form.phone_number.data
        current_attorney.about = form.about.data
        print(f"picture: {request.form.get('picture')}")
        if request.form.get('picture') != '':
            current_attorney.picture_url = request.form.get('picture')
        if form.validate():
            session.commit()
            flash('Attorney details saved', category='success')
            session.close()
            print(f'session closed')
            return redirect(url_for('employees.manage_employees'))
        else:
            flash('Changes failed to save', category='error')
    else:
        form.name.data = current_attorney.name
        form.email.data = current_attorney.email
        form.title.data = current_attorney.title
        form.phone_number.data = current_attorney.phone_number
        form.about.data = current_attorney.about
        form.picture_url.data = current_attorney.picture_url
    return render_template('create-attorney.html', public_view=False, form=form, header=header, button=button,
                           current_user=current_user, current_attorney=current_attorney)


@employees.route('/add_license', methods=['GET', 'POST'])
@login_required
def add_license():
    if request.method == 'POST':
        json_data = request.get_json()
        print(f'json object: {json_data}')
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        print(f'attorneyid: {attorney_id}, \njson_object: {json_data}')
        title = json_data[1]['title']
        new_license = AttorneyProfessionalLicense(title=title, attorney=attorney)
        session.add(new_license)
        session.flush()
        results = {'title': title,
                   'toString': new_license.to_string(),
                   'licenseId': new_license.id}
        return jsonify(results)


@employees.route('/edit_license', methods=['GET', 'POST'])
@login_required
def edit_license():
    if request.method == 'POST':
        json_data = request.get_json()
        license_id = int(json_data[0]['id'])
        new_title = json_data[1]['newTitle']
        license = session.query(AttorneyProfessionalLicense).get(license_id)
        attorney_id = license.attorney_id
        license.title = new_title
        db.session.flush()
        results = {'attorneyId': attorney_id,
                   'title': new_title,
                   'toString': license.to_string(),
                   'licenseId': license.id}
        return jsonify(results)


@employees.route('/delete_license', methods=['POST'])
@login_required
def delete_license():
    json_data = request.get_json()
    license_id = json_data[0]['licenseId']
    license = session.query(AttorneyProfessionalLicense).get(license_id)
    print(f"license to delete: {license}")
    session.delete(license)
    session.flush()
    return jsonify({'true': 'true'})


@employees.route('/add_activity', methods=['GET', 'POST'])
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


@employees.route('/edit_activity', methods=['GET', 'POST'])
@login_required
def edit_activity():
    if request.method == 'POST':
        json_data = request.get_json()
        activity_id = int(json_data[0]['activityId'])
        new_title = json_data[1]['newTitle']
        activity = session.query(AttorneyProfessionalActivity).get(activity_id)
        attorney_id = activity.attorney_id
        activity.title = new_title
        session.flush()
        results = {'attorneyId': attorney_id,
                   'activityId': activity_id,
                   'toString': activity.to_string(),
                   'activityTitle': activity.title}
        return jsonify(results)


@employees.route('/delete_activity', methods=['POST'])
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


@employees.route('/add_education', methods=['GET', 'POST'])
@login_required
def add_education():
    if request.method == 'POST':
        json_data = request.get_json()
        attorney_id = int(json_data[0]['attorneyId'])
        print(attorney_id)
        attorney = session.query(Attorney).get(attorney_id)
        print(f'current attorney: {attorney}')
        education = AttorneyEducation(degree=json_data[1]['degree'], school=json_data[2]['school'],
                                      year=json_data[3]['year'], accolades=json_data[4]['accolades'],
                                      attorney=attorney)
        print(education)
        session.add(education)
        session.flush()
        print(session.__contains__(education))
        results = {'degree': education.school,
                   'school': education.school,
                   'year': education.year,
                   'accolades': education.accolades,
                   'toString': education.to_string(),
                   'educationId': education.id}
        print(results)
        return jsonify(results)


@employees.route('/edit_education', methods=['GET', 'POST'])
@login_required
def edit_education():
    if request.method == 'POST':
        json_data = request.get_json()
        print(f'jsondata: {json_data}')
        education_id = int(json_data[0]['educationId'])
        education = session.query(AttorneyEducation).get(education_id)
        education.degree = json_data[1]['degree']
        education.school = json_data[2]['school']
        education.year = json_data[3]['year']
        education.accolades = json_data[4]['accolades']
        session.flush()
        results = {'toString': education.to_string(),
                   'degree': education.degree,
                   'school': education.school,
                   'year': education.year,
                   'accolades:': education.accolades,
                   'educationId': education_id}
        return jsonify(results)


@employees.route('/delete_education', methods=['POST'])
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


@employees.route('/add_publication', methods=['POST'])
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
                   'title': new_publication.title,
                   'details': new_publication.details,
                   'publication': new_publication.publication,
                   'year': new_publication.year,
                   'publicationId': new_publication.id}
        return jsonify(results)


@employees.route('/edit_publication', methods=['GET', 'POST'])
@login_required
def edit_publication():
    if request.method == 'POST':
        json_data = request.get_json()
        publication_id = int(json_data[0]['publicationId'])
        publication = session.query(AttorneyPublication).get(publication_id)
        publication.title = json_data[1]['title']
        publication.details = json_data[2]['details']
        publication.year = json_data[3]['year']
        publication.publication = json_data[4]['publication']
        session.flush()
        results = {'toString': publication.to_string(),
                   'title': publication.title,
                   'details': publication.details,
                   'year': publication.year,
                   'publication': publication.publication,
                   'publicationId': publication_id}
        return jsonify(results)


@employees.route('/delete_publication', methods=['POST'])
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


@employees.route('/add_aop', methods=['POST'])
@login_required
def add_aop():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        attorney_id = int(json_data[0]['attorneyId'])
        attorney = session.query(Attorney).get(attorney_id)
        name = json_data[1]['name']
        print(name)
        new_aop = AttorneyAreaOfPractice(name=name, attorney=attorney)
        session.add(new_aop)
        session.flush()
        print(f"new_aop.id: {new_aop.id}")
        print(f"new aop tostring: {new_aop.to_string()}")
        results = {'toString': new_aop.to_string(),
                   'aopName': name,
                   'aopId': new_aop.id}
        return jsonify(results)


@employees.route('/edit_aop', methods=['GET', 'POST'])
@login_required
def edit_aop():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        aop_id = int(json_data[0]['aopId'])
        new_title = json_data[1]['newName']
        print(f"newName: {new_title}")
        aop = session.query(AttorneyAreaOfPractice).get(aop_id)
        attorney_id = aop.attorney_id
        aop.title = new_title
        session.flush()
        results = {'attorneyId': attorney_id,
                   'aopId': aop.id,
                   'toString': aop.to_string(),
                   'name': aop.title}
        return jsonify(results)


@employees.route('/delete_aop', methods=['POST'])
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


@employees.route('/add_admission', methods=['POST'])
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


@employees.route('/edit_admission', methods=['GET', 'POST'])
@login_required
def edit_admission():
    if request.method == 'POST':
        json_data = request.get_json()
        admission_id = int(json_data[0]['admissionId'])
        new_court = json_data[1]['court']
        new_year = json_data[2]['year']
        admission = session.query(AttorneyAdmission).get(admission_id)
        attorney_id = admission.attorney_id
        admission.court = new_court
        admission.year = new_year
        session.flush()
        results = {'attorneyId': attorney_id,
                   'toString': admission.to_string(),
                   'admissionCourt': admission.court,
                   'admissionYear': admission.year,
                   'admissionId': admission_id}
        return jsonify(results)


@employees.route('/delete_admission', methods=['POST'])
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


@employees.route('/add_membership', methods=['POST'])
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


@employees.route('/edit_membership', methods=['GET', 'POST'])
@login_required
def edit_membership():
    if request.method == 'POST':
        json_data = request.get_json()
        membership_id = int(json_data[0]['membershipId'])
        new_name = json_data[1]['name']
        membership = session.query(AttorneyMembership).get(membership_id)
        attorney_id = membership.attorney_id
        membership.name = new_name
        session.flush()
        results = {'attorneyId': attorney_id, 'toString': membership.to_string()}
        return jsonify(results)


@employees.route('/delete_membership', methods=['POST'])
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


@employees.route('/delete_attorney/<int:aId>')
@login_required
def delete_attorney(aId):
    db.session.delete(Attorney.query.get(aId))
    db.session.commit()
    flash('Attorney was successfully deleted', category='success')
    return redirect(url_for('employees.manage_employees'))

