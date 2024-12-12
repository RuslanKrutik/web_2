from flask import Blueprint, redirect, render_template, request, make_response, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
lab4 = Blueprint('lab4', __name__)

lab4.secret_key = '1111'  # Замените на свой секретный ключ

@lab4.route('/lab4')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
        if x2 == 0:
            return render_template('lab4/div.html', error='На ноль делить нельзя!')
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/div.html', error='Введите корректные числа!')

# Суммирование
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', 0)
    x2 = request.form.get('x2', 0)
    try:
        x1 = int(x1 or 0)
        x2 = int(x2 or 0)
        result = x1 + x2
        return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/sum.html', error='Введите корректные числа!')

# Умножение
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', 1)
    x2 = request.form.get('x2', 1)
    try:
        x1 = int(x1 or 1)
        x2 = int(x2 or 1)
        result = x1 * x2
        return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/mul.html', error='Введите корректные числа!')

# Вычитание
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/sub.html', error='Введите корректные числа!')

# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
        if x1 == 0 and x2 == 0:
            return render_template('lab4/pow.html', error='Оба значения не могут быть равны нулю!')
        result = x1 ** x2
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/pow.html', error='Введите корректные числа!')


tree_count = 0
MAX_TREES = 10

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=MAX_TREES)

    operation = request.form.get('operation')
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < MAX_TREES:
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123','name': 'Саша белый'},
    {'login': 'bob', 'password': '555', 'name': 'Саша черный'},
    {'login': 'bobik', 'password': '5252', 'name': 'Саша желтый'},
    {'login': 'bobik2', 'password': '525252', 'name': 'Саша бесцветный'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if 'login' in session:
            authorized = True
            user_name = session['user_name']
            login = session['login']
        else:
            authorized = False
            user_name = ''
            login = ''
        return render_template("lab4/login.html", authorized=authorized, user_name=user_name, login=login)

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
        
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['user_name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверные логин и пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods= ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ''
    if request.method == 'POST':
        try:
            temperature = float(request.form.get('temperature'))
            if temperature < -12:
                message = "Не удалось установить температуру — слишком низкое значение."
            elif temperature > -1:
                message = "Не удалось установить температуру — слишком высокое значение."
            elif -12 <= temperature <= -9:
                message = f"Установлена температура: {temperature}°C ❄️❄️❄️"
            elif -8 <= temperature <= -5:
                message = f"Установлена температура: {temperature}°C ❄️❄️"
            elif -4 <= temperature <= -1:
                message = f"Установлена температура: {temperature}°C ❄️"  
        except ValueError:
            message = "Ошибка: не задана температура."

    return render_template("lab4/fridge.html", message=message)

# Цены на зерно
grain_prices = {
    'barley': 12345,  # Ячмень
    'oats': 8522,     # Овёс
    'wheat': 8722,    # Пшеница
    'rye': 14111      # Рожь
}

@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    message = ""
    
    if request.method == 'POST':
        grain = request.form.get('grain')
        weight = request.form.get('weight')

        if not weight:
            message = "Ошибка: вес не указан."
            return render_template("lab4/grain_order.html", message=message)
        
        try:
            weight = float(weight)

            if weight <= 0:
                message = "Ошибка: вес должен быть больше 0."
                return render_template("lab4/grain_order.html", message=message)

            if weight > 500:
                message = "Ошибка: такого объёма сейчас нет в наличии."
                return render_template("lab4/grain_order.html", message=message)

            price_per_ton = grain_prices[grain]
            total_cost = price_per_ton * weight

            # Применение скидки
            discount = 0
            if weight > 50:
                discount = total_cost * 0.1  # 10%
                total_cost -= discount
                message += "Применена скидка за большой объём: {:.2f} руб.".format(discount)

            message += "Заказ успешно сформирован. Вы заказали зерно: {}. Вес: {:.1f} т. Сумма к оплате: {:.2f} руб.".format(grain, weight, total_cost)
        except ValueError:
            message = "Ошибка: некорректный ввод веса."
            
    
    return render_template("/lab4/grain_order.html", message=message)

# Массив пользователей

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        
        # Проверка на существование логина
        for user in users:
            if user['login'] == login:
                return render_template('lab4/register.html', error='Этот логин уже занят.')
        
        # Добавление нового пользователя
        users.append({
            'login': login,
            'password': generate_password_hash(password),
            'name': name
        })
        
        return redirect(url_for('lab4.login'))  # Перенаправление на страницу входа
    
    return render_template('lab4/register.html')

@lab4.route('/lab4/users')
def user_list():
    if 'login' not in session:
        return redirect(url_for('lab4.login'))  # Переход на страницу логина, если не авторизованы
    
    return render_template('lab4/user_list.html', users=users, current_user=session['login'])

@lab4.route('/lab4/delete_user/<user_login>', methods=['POST'])
def delete_user(user_login):
    if 'login' not in session:
        return redirect(url_for('lab4.login'))

    global users
    users = [user for user in users if user['login'] != user_login]  # Удаление пользователя
    return redirect(url_for('lab4.user_list'))  # Переход обратно к списку пользователей

@lab4.route('/lab4/edit_user/<user_login>', methods=['GET', 'POST'])
def edit_user(user_login):
    if 'login' not in session:
        return redirect(url_for('lab4.login'))

    user = next((u for u in users if u['login'] == user_login), None)
    if not user:
        return redirect(url_for('lab4.user_list'))

    if request.method == 'POST':
        user['name'] = request.form['name']
        if request.form['password']:  # Изменение пароля только если поле не пустое
            user['password'] = generate_password_hash(request.form['password'])
        return redirect(url_for('lab4.user_list'))
    
    return render_template('lab4/edit_user.html', user=user)
