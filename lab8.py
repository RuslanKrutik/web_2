from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user


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
    return redirect('/lab8/')
@lab8.route('/lab8/login', methods = ['GET', 'POST'])

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/login.html', error="Имя пользователя не должно быть пустым")
    if not password_form:
        return render_template('lab8/login.html', error="Пароль не должен быть пустым")
    
    # Проверка существования пользователя
    user = users.query.filter_by(login=login_form).first()
    
    # Проверка пароля
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=False)
            return redirect('/lab8/')
        else:
            return render_template('lab8/login.html', error="Ошибка входа: логин или пароль неверны")
    else:
        return render_template('lab8/login.html', error="Ошибка входа: пользователь не найден")

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "список статей"
