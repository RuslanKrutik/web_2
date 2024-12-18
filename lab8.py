from flask import Blueprint, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from db import db
from db.models import users, articles


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))

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