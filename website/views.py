from flask import Blueprint, render_template, abort, request, flash, g, url_for
from flask_login import current_user, login_required
from flask_mail import Message
from sqlalchemy import desc
from werkzeug.utils import redirect

from . import db, mail
from .forms import ContactForm, ArticleForm
from .models import Article

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", edit_mode=current_user.is_authenticated)


@views.route('/firm-overview')
def firm_overview():
    return render_template("firm-overview.html")


@views.route('/our-team')
def our_team():
    return render_template("our-team.html")


@views.route('david-wise')
def david_wise():
    return render_template("david-wise.html")


@views.route('joe-langone')
def joe_langone():
    return render_template("joe-langone.html")


@views.route('pat-donahue')
def pat_donahue():
    return render_template("pat-donahue.html")


@views.route('david-reese')
def david_reese():
    return render_template("david-reese.html")


@views.route('/class-actions')
def class_actions():
    return render_template("class-actions.html")


@views.route('/construction-law')
def construction_law():
    return render_template("construction-law.html")


@views.route('/construction-litigation')
def construction_litigation():
    return render_template("construction-litigation.html")


@views.route('/construction-defect-litigation')
def construction_defect_litigation():
    return render_template("construction-defect-litigation.html")


@views.route('/wrongful-death')
def wrongful_death():
    return render_template("wrongful-death.html")


@views.route('/commercial-and-business')
def commercial_and_business():
    return render_template("commercial-and-business.html")


@views.route('/mold-and-environmental')
def mold_and_environmental():
    return render_template("mold-and-environmental.html")


@views.route('/government-contracts')
def government_contracts():
    return render_template("government-contracts.html")


@views.route('/insurance-coverage')
def insurance_coverage():
    return render_template("insurance-coverage.html")


@views.route('/reviews')
def reviews():
    return render_template("reviews.html")


@views.route('/articles/<int:id>')
def articles(id=0):
    if id is 0:
        article = get_first_article()
    else:
        article = Article.query.get_or_404(id)
    articles = Article.query.all()
    return render_template("articles.html", articles=articles, article=article, logged_in=current_user.is_authenticated)


def get_first_article():
    return Article.query.order_by(desc(Article.date)).first()


@views.route('/create', methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm(request.form)
    if request.method == 'GET':
        return render_template("new-article.html")
    else:
        article = Article(title=form.title.data, text=form.text.data, date=form.date_created,
                          published_date=form.publishing_date.data, user_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('views.articles', id=article.id))


@views.route('/delete-article/<int:id>', methods=['GET', 'POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash("Article was successfully deleted!")
    return redirect(url_for('views.articles'))


@views.route('articles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    form = ArticleForm(request.form)
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = form.title.data
        article.text = form.text.data
        article.date = form.publishing_date.data
        db.session.commit()
        return redirect(url_for('views.articles', id=id))
    return render_template('edit-article.html', form=form, article=article)


@views.route('careers')
def careers():
    return render_template("careers.html")


@views.route('/maps')
def maps():
    return render_template("maps.html")


@views.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm(request.form)
    if request.method == 'POST':
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
    return render_template("contact-us.html", form=form)
