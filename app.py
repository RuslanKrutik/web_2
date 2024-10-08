from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/lab1")
def lab1():
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
@app.route("/")
@app.route("/index")
def index():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
        <body>
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            </header>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                </ul>
            </nav>
            <footer>
                <p>ФИО: Крутиков Руслан Олегович</p>
                <p>Группа: ФБИ-21</p>
                <p>Курс: 2</p>
                <p>Год: 2024</p>
            </footer>
        </body>
    </html>
    '''
@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")
        
@app.route("/lab1/oak")
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

@app.route('/lab1/reset_counter')
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
@app.route('/lab1/counter')
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

@app.route("/lab1/created")
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

@app.errorhandler(402)
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
    
@app.route('/lab1/error')
def error():
    # Это вызовет ошибку деления на ноль
    result = 1 / 0
    return f"Результат: {result}"

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

@app.route('/lab1/custom')
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