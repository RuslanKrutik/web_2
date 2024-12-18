from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/register.html', error="Имя пользователя не должно быть пустым")
    if not password_form:
        return render_template('lab8/register.html', error="Пароль не должен быть пустым")

    # Проверка на существующего пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error="Такой пользователь уже существует")
    
    # Хеширование пароля и добавление пользователя в БД
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Автоматический логин
    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'
    
    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/login.html', error="Имя пользователя не должно быть пустым")
    if not password_form:
        return render_template('lab8/login.html', error="Пароль не должен быть пустым")
    
    # Проверка существования пользователя
    user = users.query.filter_by(login=login_form).first()
    
    # Проверка пароля
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab8/')
    else:
        return render_template('lab8/login.html', error="Ошибка входа: логин или пароль неверны")
    
@lab8.route('/lab8/articles/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        
        # Проверка на заполненность полей
        if not title or not article_text:
            return render_template('lab8/create_article.html', error="Заполните все поля")
        
        # Добавление статьи в базу
        new_article = articles(title=title, article_text=article_text, login_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        return redirect('/lab8/articles/')
    
    return render_template('lab8/create_article.html')

@lab8.route('/lab8/articles/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        return "Статья не найдена или у вас нет прав для редактирования", 403

    if request.method == 'POST':
        article.title = request.form.get('title')
        article.article_text = request.form.get('article_text')
        db.session.commit()
        return redirect('/lab8/articles/')

    return render_template('lab8/edit_article.html', article=article)

@lab8.route('/lab8/articles/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        return "Статья не найдена или у вас нет прав для удаления", 403

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')
