from flask import (
    Flask,
    render_template,
    flash,
    get_flashed_messages,
    request,
    url_for,
    redirect
)
from validators import url as validate_url
from dotenv import load_dotenv
import os
import page_analyzer.database as db
from page_analyzer.models import Url


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls_index():
    conn = db.get_connection()
    repo = db.UrlRepository(conn)
    return render_template('urls/index.html', urls=repo.get_all())

@app.route('/urls', methods=['POST'])
def urls_post():
    url_name = request.form.get('url')
    if not validate_url(url_name):
        flash('Неверный URL', category='error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

    conn = db.get_connection()
    repo = db.UrlRepository(conn)
    url = repo.find(url_name=url_name)
    if not url:
        url = repo.save(Url(url_name))
        db.commit(conn)
        flash('Страница успешно добавлена', category='success')
        print('flash added')
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template(
        'urls/show.html',
        url=url, messages=messages)

@app.route('/urls/<url_id>', methods=['GET'])
def urls_get(url_id):
    conn = db.get_connection()
    repo = db.UrlRepository(conn)
    url = repo.find(url_id=url_id)
    if not url:
        return render_template('404.html'), 404
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls/show.html',
        url=url,
        url_checks=db.UrlChecksRepository(conn).get_all(url),
        messages=messages)

@app.route('/urls/<url_id>/checks', methods=['POST'])
def urls_checks(url_id):
    conn = db.get_connection()
    urls_repo = db.UrlRepository(conn)
    url = urls_repo.find(url_id=url_id)

    if not url:
        return render_template('404.html'), 404

    url_checks_repo = db.UrlChecksRepository(conn)
    url_checks_repo.save(url)
    db.commit(conn)
    flash('Страница успешно проверена','success')
    return redirect(url_for('urls_get', url_id=url_id)), 302


