import base64
import os
import re
import sqlite3
from flask import Blueprint, render_template, abort, request, flash, g, url_for
from flask_login import current_user
from flask_mail import Message
from werkzeug.utils import redirect

from . import db, DB_NAME, mail
from .models import Article

views = Blueprint('views', __name__)


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


@views.route('/')
def home():
    edit_mode = False
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        if current_user.is_authenticated():
            # Admin is signed in
            edit_mode = True
    print(edit_mode)

    return render_template("home.html", edit_mode=edit_mode)


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


def get_db():
    conn = getattr(g, '_database', None)
    if conn is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, DB_NAME)
        conn = g._database = sqlite3.connect(db_path)
    return conn


@views.route('/articles/<int:id>')
def articles(id):
    if id == 0:
        id = get_first_article()
    db = get_db()
    articles = db.execute(
        'SELECT a.id, title, text, date, user_id'
        ' FROM article a'
        ' ORDER BY date DESC'       #  articles = Article.query.order_by(Article.date.desc())
    ).fetchall()
    article = db.execute(
        'SELECT * FROM article WHERE id = ?', [id]
    ).fetchall()[0]
    print("Article to be displayed:")
    print(article)
    print(current_user.is_authenticated)
    return render_template("articles.html", articles=articles, article=article, logged_in=current_user.is_authenticated)


def create_article(conn, article):
    """
    Create a new article into the articles table
    :param conn:
    :param article:
    :return: article id
    """
    sql = ''' INSERT INTO article(title, date, text, user_id)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    print(article.text)
    cur.execute(sql, (article.title, article.date, article.text, article.user_id))
    conn.commit()
    return cur.lastrowid


@views.route('/create', methods=['GET', 'POST'])
def new_article():
    if request.method == 'GET':
        return render_template("new-article.html")
    else:
        conn = get_db()
        with conn:
            print(request.form)
            article = Article(title=request.form.get('title'), text=request.form.get('text'),
                              date=request.form.get('date'), user_id=current_user.id)
            print(article.title)
            article.id = create_article(conn, article)
            return redirect(url_for('views.articles', id=article.id))


@views.route('/delete-article/<int:id>', methods=['GET', 'POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    print("Article to Delete:")
    print(article)
    #try:
    db.session.delete(article)
    db.session.commit()
    flash("Article was successfully deleted!")
    return redirect(url_for('views.articles', id=get_first_article()))

    #except:
     #   flash("Whoops! There was a problem deleting the post.")
      #  return redirect(url_for('views.articles', id=1))


def get_first_article():
    # article = Article.query.order_by(Article.date.desc()).first()
    db = get_db()
    article = db.execute(
        'SELECT *'
        ' FROM article a'
        ' ORDER BY date DESC'  # articles = Article.query.order_by(Article.date.desc())
    ).fetchall()[0]
    return article[0]


@views.route('articles/update')
def update_article():
    return articles()


@views.route('careers')
def careers():
    return render_template("careers.html")


@views.route('/maps')
def maps():
    return render_template("maps.html")


@views.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        body = "Contact Email: " + request.form.get('email') + "\n\nMessage: \n\n" + request.form.get('message')
        title = "WLF website: New Message from " + request.form.get('name')
        msg = Message(title,
                      body=body,
                      sender=request.form.get('email'),
                      recipients=['cwise@wiselaw.pro'])
        print(msg)
        mail.send(msg)
        flash("Message was successfully sent!")
        return redirect(url_for('views.home'))
    return render_template("contact-us.html")


@views.route('/x/save-page', methods=['POST'])
def save_page():
    """Save changes to a page"""
    html_root = os.path.abspath('website\\templates')
    # Find the page
    filename = request.form['__page__']
    if filename == '/':
        filename = 'home'  # The home page will appear as ''
    elif filename.startswith('/'):
        # remove leading '/'
        filename = filename[1:]
    filename = 'website\\templates\\' + filename + '.html'

    print(html_root)
    print(filename)
    # Is the filename safe to access?
    if not os.path.abspath(filename).startswith(html_root):
        print("FAILED 1")
        abort(404)

    # Do we have an HTML file to match the URL?
    if not os.path.exists(filename.strip()):
        print("FAILED 2")
        abort(404)

    # Read the contents of the HTML file and update it
    with open(filename, 'r', encoding='cp1252') as f:
        html = f.read()

        # For each parameter in the request attempt to match and replace the
        # value in the HTML.
        for name, value in request.form.items():

            # Escape backslashes in the value for regular expression use
            value = value.replace('\\', '\\\\')

            # Match and replace editable regions
            start_tag = '<!--\s*editable\s+' + re.escape(name) + '\s*-->'
            end_tag = '<!--\s*endeditable\s+' + re.escape(name) + '\s*-->'
            html = re.sub(
                '({0}\s*)(.*?)(\s*{1})'.format(start_tag, end_tag),
                r'\1' + value + r'\3',
                html,                           # template_html????
                flags=re.DOTALL
                )

    # Save changes to the HTML file
    with open(filename, 'w', encoding='cp1252') as f:
        f.write(html)

    return 'saved'
