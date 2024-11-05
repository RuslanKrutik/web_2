from flask import Blueprint, url_for, redirect, abort
from werkzeug.exceptions import HTTPException
lab1 = Blueprint('lab1', __name__)

class PaymentRequired(HTTPException):
    code = 402
    description = "Требуется оплата."


@lab1.route("/lab1")
def lab():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
        </head>
        <body>
            <p>
                Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится 
                к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
                сознательно предоставляющих лишь самые базовые возможности.
            </p>
            <a href="/">Назад на главную</a>
            <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1">Лабораторная 1</a></li>
                <li><a href="/lab1/counter">Счётчик</a></li>
                <li><a href="/lab1/reset_counter">Очистить счётчик</a></li>
                <li><a href="/lab1/oak">Дуб</a></li>
                <li><a href="/lab1/error">Ошибка</a></li>
                <li><a href="/lab1/custom">Пользовательская страница</a></li>
                <li><a href="/lab1/web">На чем написан сервер</a></li>
                <li><a href="/lab1/author">Автор</a></li>
                <li><a href="/lab1/created">201</a></li>
            </ul>
            </ul>
        </body>
    </html>
    '''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
    <html>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="/lab1/author">author</a>
        </body>
    </html>""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }


@lab1.route("/lab1/author")
def author():
    name = "Крутиков Руслан Олегович"
    group = "ФБИ-21"
    faculty = "ФБ"
    
    return f"""<!doctype html>
    <html>
        <body>
            <p>Студент: {name}</p>
            <p>Группа: {group}</p>
            <p>Факультет: {faculty}</p>
            <a href="/lab1/web">web</a>
        </body>
    </html>"""


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <h1>Дуб</h1>
            <img src="{path}">
        </body>
    </html>
    '''


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
    <!doctype html>
    <html>
        <body>
            <p>Счётчик был очищен!</p>
            <a href="/lab1/counter">Назад к счётчику</a>
        </body>
    </html>'''


count = 0 
@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    return f'''
    <!doctype html>
    <html>
        <body>
            <p>Сколько раз вы сюда заходили: {count}</p>
            <a href="/lab1/reset_counter">Очистить счётчик</a>
        </body>
    </html>'''


@lab1.route("/lab1/created")
def created():
    return '''
        <!doctype html>
        <html>
            <body>
                <h1>Создано успешно</h1>
                <div><i>что-то создано...<i></div>
            </body>
        </html>
        ''', 201


@lab1.route('/lab1/error')
def error():
    # Это вызовет ошибку деления на ноль
    result = 1 / 0
    return f"Результат: {result}"


@lab1.route('/lab1/custom')
def custom_route():
    img_path = url_for("static", filename="example.webp")
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Моя пользовательская страница</title>
        </head>
        <body>
            <h1>Человек</h1>
            <p>Челове́к — общественное существо, обладающее разумом и сознанием, субъект общественно-исторической деятельности и культуры.</p>
            <p>Стремление человека постигать окружающий мир, его явления и их влияние на жизнь привело к возникновению науки и технологий.</p>
            <p>У человека разумного большая, чрезвычайно развитая и сложная префронтальная кора — область мозга, связанная с высшими когнитивными способностями.</p>
            <img src="''' + img_path + '''" alt="Пример изображения">
        </body>
    </html>
    ''', 200, {
        'LanguageSSS+': 'ru',
        'Header_228': 'CustomValue1',
        'X_X': 'Flask'
    }


@lab1.route("/lab1/error400")
def error400():
    return abort(400)