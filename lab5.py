from flask import Blueprint, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def db_close(conn):
    conn.commit()
    conn.close()

@lab5.route('/lab5')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        if not (login and password):
            return render_template('lab5/register.html', error='Заполните все поля')
        
        conn, cur = db_connect()
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
        
        if cur.fetchone():
            db_close(conn)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES(?, ?);", (login, password_hash))
        db_close(conn)
        return render_template('lab5/success.html', login=login)
    
    return render_template('lab5/register.html')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        if not (login and password):
            return render_template('lab5/login.html', error="Заполните поля")
        
        conn, cur = db_connect()
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        
        if not user or not check_password_hash(user['password'], password):
            db_close(conn)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        db_close(conn)
        return redirect('/lab5')
    
    return render_template('lab5/login.html')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        
        if not title or not article_text:
            return render_template('lab5/create_article.html', error="Тема или текст не могут быть пустыми")
        
        conn, cur = db_connect()
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        user_id = cur.fetchone()["id"]
        
        cur.execute("INSERT INTO articles(login_id, title, article_text) VALUES(?, ?, ?)",
                    (user_id, title, article_text))
        db_close(conn)
        return redirect('/lab5')
    
    return render_template('lab5/create_article.html')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    cur.execute("SELECT * FROM articles WHERE login_id=?", (user_id,))
    articles = cur.fetchall()
    db_close(conn)
    
    if not articles:
        return render_template('lab5/articles.html', articles=None, message="У вас нет статей.")
    
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            return render_template('lab5/edit_article.html', error="Тема или текст не могут быть пустыми", article_id=article_id)

        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?", (title, article_text, article_id))
        db_close(conn)
        return redirect('/lab5/list')

    cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()
    db_close(conn)
    
    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM articles WHERE id=?", (article_id,))
    db_close(conn)
    return redirect('/lab5/list')
