from flask import Blueprint, redirect, render_template, request, make_response
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

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    if color:
        resp = make_response(redirect('lab3/settings'))
        resp.set_cookie('color', color)
        return resp

    color = request.args.get('color')
    resp = make_response(render_template('lab3/settings.html', color=color))
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