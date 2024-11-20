from flask import Blueprint, redirect, render_template, request, make_response, url_for
lab4 = Blueprint('lab4', __name__)

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

