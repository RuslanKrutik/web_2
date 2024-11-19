from flask import Blueprint, redirect, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route("/lab2/a")
def a():
    return 'без сэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цвета нет", 404
    else:
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Цветок: {flower_list[flower_id]}</h1>
            <a href="/lab2/flowers">Посмотреть все цветы</a>
            </body>
        </html>
        '''


@lab2.route('/lab2/add_flower/<name>')
def add_flower(name=None):
    if not name:  # Проверка на пустое имя
        return "вы не задали имя цветка", 400
    
    flower_list.lab2end(name)
    return f'''
    <!doctype html>
    <html>
        <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
        </body>
    </html>
    '''
@lab2.route('/lab2/flowers')
def list_flowers():
    return f'''
    <!doctype html>
    <html>
        <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {''.join([f"<li>{flower}</li>" for flower in flower_list])}
        </ul>
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
        </body>
    </html>
    '''
@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
    <!doctype html>
    <html>
        <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
        </body>
    </html>
    '''

@lab2.route('/lab2/example')
def example():
    name = 'Крутиков Руслан'
    n_group = "21"
    n_kurs = "3"
    n_lab = "2"
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html',
                        name=name, n_group=n_group, 
                        n_kurs=n_kurs, n_lab=n_lab,
                        fruits=fruits)
@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html'), {'Accept-Language': 'ru-RU'}

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filters.html', phrase = phrase)

# Маршрут для обработки двух чисел и выполнения операций
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template("lab2/calc.html", a=a, b=b)

# Маршрут для перенаправления на значения по умолчанию (1, 1)
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

# Маршрут для перенаправления с одного числа на пару (a, 1)
@lab2.route('/lab2/calc/<int:a>')
def calc_with_one(a):
    return redirect(f'/lab2/calc/{a}/1')

# Список книг на стороне сервера с добавлением американских авторов
books = [
    {"author": "Антон Чехов", "title": "Чайка", "genre": "Пьеса", "pages": 128},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 480},
    {"author": "Марк Твен", "title": "Приключения Тома Сойера", "genre": "Приключения", "pages": 240},
    {"author": "Эрнест Хемингуэй", "title": "Старик и море", "genre": "Новелла", "pages": 132},
    {"author": "Фрэнсис Скотт Фицджеральд", "title": "Великий Гэтсби", "genre": "Роман", "pages": 180},
    {"author": "Джек Лондон", "title": "Зов предков", "genre": "Приключения", "pages": 232},
    {"author": "Джон Стейнбек", "title": "Гроздья гнева", "genre": "Роман", "pages": 464},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 389}
    
]
# Обработчик для отображения списка книг
@lab2.route('/lab2/books')
def show_books():
    return render_template("lab2/books.html", books=books)

# Список ягод с описанием и ссылками на изображения
# Список ягод с описанием и ссылками на изображения
berries = [
    {"name": "Клубника", "image": "images/strawberry.jpg", "description": "Сладкая красная ягода, любимая многими."},
    {"name": "Голубика", "image": "images/blueberry.webp", "description": "Маленькая синяя ягода с богатым вкусом."},
    {"name": "Малина", "image": "images/raspberry.jpg", "description": "Сочная и ароматная красная ягода."},
    {"name": "Черника", "image": "images/blackberry.jpg", "description": "Сладкая и полезная темно-синяя ягода."},
    {"name": "Клюква", "image": "images/cranberry.jpg", "description": "Кислая красная ягода, часто используется в напитках."}
]

@lab2.route('/lab2/berries')
def show_berries():
    return render_template("lab2/berries.html", berries=berries)
