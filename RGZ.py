from flask import Blueprint, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

RGZ = Blueprint('RGZ', __name__)

# Функции для работы с БД
def db_connect():
    """
    Подключение к базе данных SQLite.
    """
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "messenger.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    """
    Закрытие подключения к базе данных.
    """
    conn.commit()
    cur.close()
    conn.close()

# Роуты
@RGZ.route('/welcome/')
def welcome():
    return render_template('welcome.html')

@RGZ.route('/json-rpc-api/', methods=['POST'])
def json_rpc_api():
    """
    JSON-RPC API endpoint.
    """
    data = request.json
    method = data.get('method')
    params = data.get('params', {})
    rpc_id = data.get('id')

    if method == 'register_user':
        return register_user(params, rpc_id)
    elif method == 'login_user':
        return login_user(params, rpc_id)
    elif method == 'get_users':
        return get_users(params, rpc_id)
    else:
        return error_response(rpc_id, -32601, 'Method not found')

# Методы API
def register_user(params, rpc_id):
    """
    Регистрация пользователя.
    """
    username = params.get('username')
    password = params.get('password')

    if not username or not password:
        return error_response(rpc_id, 1, 'Username and password are required.')

    conn, cur = db_connect()
    cur.execute("SELECT id FROM user WHERE username = ?", (username,))
    if cur.fetchone():
        db_close(conn, cur)
        return error_response(rpc_id, 2, 'Username already exists.')

    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO user (username, password_hash) VALUES (?, ?)", (username, password_hash))
    db_close(conn, cur)

    return success_response(rpc_id, 'User registered successfully.')

def login_user(params, rpc_id):
    """
    Авторизация пользователя.
    """
    username = params.get('username')
    password = params.get('password')

    if not username or not password:
        return error_response(rpc_id, 1, 'Username and password are required.')

    conn, cur = db_connect()
    cur.execute("SELECT id, password_hash FROM user WHERE username = ?", (username,))
    user = cur.fetchone()

    if not user or not check_password_hash(user["password_hash"], password):
        db_close(conn, cur)
        return error_response(rpc_id, 3, 'Invalid username or password.')

    session_token = generate_password_hash(f"{username}")
    cur.execute("INSERT INTO session (token, user_id) VALUES (?, ?)", (session_token, user["id"]))
    db_close(conn, cur)

    return success_response(rpc_id, {'token': session_token})

def get_users(params, rpc_id):
    """
    Получение списка пользователей.
    """
    token = params.get('token')

    if not token or not validate_session(token):
        return error_response(rpc_id, 4, 'Unauthorized.')

    conn, cur = db_connect()
    cur.execute("SELECT id, username FROM user")
    users = [{"id": row["id"], "username": row["username"]} for row in cur.fetchall()]
    db_close(conn, cur)

    return success_response(rpc_id, {'users': users})

# Вспомогательные функции
def validate_session(token):
    """
    Проверяет валидность сессии.
    """
    conn, cur = db_connect()
    cur.execute("SELECT id FROM session WHERE token = ?", (token,))
    session_exists = cur.fetchone() is not None
    db_close(conn, cur)
    return session_exists

def success_response(rpc_id, result):
    """
    Формирует успешный ответ JSON-RPC.
    """
    return {
        'jsonrpc': '2.0',
        'result': result,
        'id': rpc_id
    }

def error_response(rpc_id, code, message):
    """
    Формирует ошибочный ответ JSON-RPC.
    """
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': code,
            'message': message
        },
        'id': rpc_id
    }