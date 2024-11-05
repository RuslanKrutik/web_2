from flask import Blueprint, redirect, render_template
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    return render_template('lab3.html'), {'Accept-Language': 'ru-RU'}

@lab3.route('/lab3/cookie')
def cookie():
    return 'cookie!!!'