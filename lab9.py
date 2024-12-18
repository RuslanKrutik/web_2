from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

# Страница 1: Ввод имени
@lab9.route('/lab9', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.step2', name=name))
    return render_template('lab9/step1.html')

# Страница 2: Ввод возраста
@lab9.route('/lab9/step2', methods=['GET', 'POST'])
def step2():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.step3', name=name, age=age))
    return render_template('lab9/step2.html', name=name)

# Страница 3: Ввод пола
@lab9.route('/lab9/step3', methods=['GET', 'POST'])
def step3():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.step4', name=name, age=age, gender=gender))
    return render_template('lab9/step3.html', name=name, age=age)

# Страница 4: Первый вопрос
@lab9.route('/lab9/step4', methods=['GET', 'POST'])
def step4():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        choice1 = request.form.get('choice1')
        return redirect(url_for('lab9.step5', name=name, age=age, gender=gender, choice1=choice1))
    return render_template('lab9/step4.html', name=name, age=age, gender=gender)

# Страница 5: Второй вопрос
@lab9.route('/lab9/step5', methods=['GET', 'POST'])
def step5():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    choice1 = request.args.get('choice1')
    if request.method == 'POST':
        choice2 = request.form.get('choice2')
        return redirect(url_for('lab9.result', name=name, age=age, gender=gender, choice1=choice1, choice2=choice2))
    return render_template('lab9/step5.html', name=name, age=age, gender=gender, choice1=choice1)

# Страница 6: Поздравление
@lab9.route('/lab9/result', methods=['GET'])
def result():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    choice1 = request.args.get('choice1')
    choice2 = request.args.get('choice2')
    
    # Логика поздравления
    is_child = age < 18
    if choice1 == 'tasty':
        if choice2 == 'sweet':
            gift = 'новый айфон'
            image = 'iphone.webp'
        else:
            gift = 'аппетитный бургер'
            image = 'burger.webp'
    else:
        gift = 'красивая открытка'
        image = 'card.webp'

    wish = f"Поздравляю тебя, {name}, желаю, чтобы ты стал богатым когда вырастишь !" if is_child else f"Поздравляю вас, {name}, желаю здоровья и счастья"
    if gender == 'female':
        wish = wish.replace("стал", "стала")
    
    return render_template('lab9/result.html', name=name, wish=wish, gift=gift, image=image)