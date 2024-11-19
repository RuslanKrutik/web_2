from flask import Blueprint, redirect, render_template, request, make_response, url_for
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3')
def lab():
    name = request.cookies.get('name', 'аноним')
    age = request.cookies.get('age', 'неизвестный')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color), {'Accept-Language': 'ru-RU'}


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def cookie_del():
    resp=make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors= {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/orders')
def orders():
    return render_template('lab3/orders.html')
    
@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, черный чай - 80 рублей, зеленый - 70 рублей
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    # Добавка молока удорожает напиток на 30 рублей, а сахар - на 10
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success_pay')
def success_pay():
    return render_template('lab3/success_pay.html')


@lab3.route('/lab3/settings', methods=['GET'])
def settings():
    color = request.args.get('color')
    if color:
        # Устанавливаем cookie для цвета
        resp = make_response(redirect(url_for('lab3.settings')))
        resp.set_cookie('color', color)
        return resp

    # Получаем значение цвета из cookies
    color = request.cookies.get('color')
    return render_template('lab3/settings.html', color=color)

@lab3.route('/lab3/clear_cookies', methods=['GET'])
def clear_cookies():
    # Очищаем все cookies
    resp = make_response(redirect(url_for('lab3.settings')))
    for cookie in request.cookies:
        resp.delete_cookie(cookie)
    return resp


@lab3.route('/lab3/train_ticket', methods=['GET', 'POST'])
def train_ticket():
    if request.method == 'GET':
        return render_template('lab3/train_ticket_form.html')

    # Обработка данных формы
    fullname = request.form.get('fullname')
    berth = request.form.get('berth')
    linen = request.form.get('linen') == 'on'
    baggage = request.form.get('baggage') == 'on'
    age = int(request.form.get('age'))
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    trip_date = request.form.get('trip_date')
    insurance = request.form.get('insurance') == 'on'

    # Валидация данных
    errors = []
    if not fullname or not departure or not destination or not trip_date:
        errors.append("Все поля должны быть заполнены.")
    if not (1 <= age <= 120):
        errors.append("Возраст должен быть от 1 до 120 лет.")

    if errors:
        return render_template('lab3/train_ticket_form.html', errors=errors)

    # Расчет стоимости
    base_price = 700 if age < 18 else 1000
    if berth in ["нижняя", "нижняя боковая"]:
        base_price += 100
    if linen:
        base_price += 75
    if baggage:
        base_price += 250
    if insurance:
        base_price += 150
    
    # Формирование билета
    ticket_info = {
        "fullname": fullname,
        "age": age,
        "type": "Детский билет" if age < 18 else "Взрослый билет",
        "departure": departure,
        "destination": destination,
        "trip_date": trip_date,
        "berth": berth,
        "linen": linen,
        "baggage": baggage,
        "insurance": insurance,
        "price": base_price
    }

    return render_template('lab3/train_ticket_result.html', ticket=ticket_info)

cars = [
    {"name": "BMW 1 Series", "price": 2000000, "color": "White", "engine": "1.5L"},
    {"name": "BMW 2 Series", "price": 2500000, "color": "Black", "engine": "2.0L"},
    {"name": "BMW 3 Series", "price": 3000000, "color": "Blue", "engine": "2.0L"},
    {"name": "BMW 4 Series", "price": 3500000, "color": "Red", "engine": "2.0L"},
    {"name": "BMW 5 Series", "price": 4000000, "color": "Silver", "engine": "3.0L"},
    {"name": "BMW 6 Series", "price": 4500000, "color": "White", "engine": "3.0L"},
    {"name": "BMW 7 Series", "price": 5000000, "color": "Black", "engine": "3.5L"},
    {"name": "BMW X1", "price": 2600000, "color": "Blue", "engine": "2.0L"},
    {"name": "BMW X2", "price": 3100000, "color": "Red", "engine": "2.0L"},
    {"name": "BMW X3", "price": 3600000, "color": "Silver", "engine": "3.0L"},
    {"name": "BMW X4", "price": 4100000, "color": "White", "engine": "3.0L"},
    {"name": "BMW X5", "price": 4600000, "color": "Black", "engine": "3.5L"},
    {"name": "BMW X6", "price": 5100000, "color": "Blue", "engine": "3.5L"},
    {"name": "BMW X7", "price": 5600000, "color": "Silver", "engine": "4.0L"},
    {"name": "BMW Z4", "price": 3800000, "color": "Red", "engine": "3.0L"},
    {"name": "BMW M3", "price": 6000000, "color": "Black", "engine": "4.0L"},
    {"name": "BMW M4", "price": 6500000, "color": "Blue", "engine": "4.0L"},
    {"name": "BMW M5", "price": 7000000, "color": "Silver", "engine": "4.4L"},
    {"name": "BMW i3", "price": 2800000, "color": "White", "engine": "Electric"},
    {"name": "BMW i8", "price": 12000000, "color": "Black", "engine": "Hybrid"},
]

# Главная страница с формой для фильтрации
@lab3.route('/lab3/cars', methods=['GET', 'POST'])
def cars_filter():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    
    # Фильтрация автомобилей по цене
    filtered_cars = []
    if min_price is not None and max_price is not None:
        filtered_cars = [
            car for car in cars if min_price <= car["price"] <= max_price
        ]

    return render_template('lab3/cars.html', cars=filtered_cars, min_price=min_price, max_price=max_price)