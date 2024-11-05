from flask import Flask, url_for, redirect, abort, render_template
from werkzeug.exceptions import HTTPException
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
class PaymentRequired(HTTPException):
    code = 402
    description = "Требуется оплата."

@app.route("/")
@app.route("/index")
def index():
    return render_template('menu.html')

@app.errorhandler(400)
def bad_request_error(error):
    return '''
    <!doctype html>
    <html>
        <head><title>400 Bad Request</title></head>
        <body>
            <h1>400 Bad Request</h1>
            <p>Некорректный запрос.</p>
        </body>
    </html>
    ''', 400

@app.errorhandler(401)
def unauthorized_error(error):
    return '''
    <!doctype html>
    <html>
        <head><title>401 Unauthorized</title></head>
        <body>
            <h1>401 Unauthorized</h1>
            <p>Требуется авторизация.</p>
        </body>
    </html>
    ''', 401

@app.errorhandler(PaymentRequired)
def payment_required_error(error):
    return '''
    <!doctype html>
    <html>
        <head><title>402 Payment Required</title></head>
        <body>
            <h1>402 Payment Required</h1>
            <p>Требуется оплата.</p>
        </body>
    </html>
    ''', 402

@app.errorhandler(403)
def forbidden_error(error):
    return '''
    <!doctype html>
    <html>
        <head><title>403 Forbidden</title></head>
        <body>
            <h1>403 Forbidden</h1>
            <p>Доступ запрещен.</p>
        </body>
    </html>
    ''', 403

@app.errorhandler(405)
def method_not_allowed_error(error):
    return '''
    <!doctype html>
    <html>
        <head><title>405 Method Not Allowed</title></head>
        <body>
            <h1>405 Method Not Allowed</h1>
            <p>Метод не разрешен.</p>
        </body>
    </html>
    ''', 405

@app.errorhandler(418)
def teapot_error(error):
    return '''
    <!doctype html>
    <html>
        <head><title>418 I'm a teapot</title></head>
        <body>
            <h1>418 I'm a teapot</h1>
            <p>Я чайник. Не могу заварить кофе.</p>
        </body>
    </html>
    ''', 418

@app.errorhandler(404)
def not_found_error(error):
    css_path = url_for("static", filename="error.css")
    img_path = url_for("static", filename="404.jpeg")
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>404 Страница не найдена</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <h1>404 Ошибка</h1>
            <p>Упс! Кажется, вы заблудились.</p>
            <img src="{img_path}" alt="404">
            <p>К сожалению, страница, которую вы ищете, не найдена.</p>
            <a href="/">Вернуться на главную</a>
        </body>
    </html>
    ''', 404

@app.errorhandler(500)
def internal_error(error):
    return '''
    <!doctype html>
    <html>
        <head>
            <title>500 Внутренняя ошибка сервера</title>
        </head>
        <body>
            <h1>500 Внутренняя ошибка сервера</h1>
            <p>На сервере произошла ошибка. Пожалуйста, попробуйте позже.</p>
            <a href="/">Вернуться на главную</a>
        </body>
    </html>
    ''', 500