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
    return render_template('RGZ/welcome.html')

@RGZ.route('/confirmation/')
def confirmation():
    return render_template('RGZ/confirmation.html')

@RGZ.route('/users/')
def users():
    """
    Маршрут для отображения списка пользователей.
    """
    return render_template('RGZ/users.html')

@RGZ.route('/chat/')
def chat():
    """
    Маршрут для отображения чата.
    """
    return render_template('RGZ/chat.html')

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
    elif method == 'send_message':
        return send_message(params, rpc_id)
    elif method == 'get_messages':
        return get_messages(params, rpc_id)
    elif method == 'delete_message':
        return delete_message(params, rpc_id)
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
    Получение списка пользователей, исключая самого пользователя.
    """
    token = params.get('token')

    user_id = validate_session(token)
    if not user_id:
        return error_response(rpc_id, 4, 'Unauthorized.')

    conn, cur = db_connect()
    cur.execute("SELECT id, username FROM user WHERE id != ?", (user_id,))
    users = [{"id": row["id"], "username": row["username"]} for row in cur.fetchall()]
    db_close(conn, cur)

    return success_response(rpc_id, {'users': users})

def send_message(params, rpc_id):
    """
    Отправка сообщения.
    """
    token = params.get('token')
    receiver_id = params.get('receiver_id')
    text = params.get('text')

    user_id = validate_session(token)
    if not user_id:
        return error_response(rpc_id, 4, 'Unauthorized.')

    if not receiver_id or not text:
        return error_response(rpc_id, 1, 'Receiver ID and text are required.')

    conn, cur = db_connect()
    cur.execute(
        "INSERT INTO message (sender_id, receiver_id, text) VALUES (?, ?, ?)",
        (user_id, receiver_id, text)
    )
    db_close(conn, cur)

    return success_response(rpc_id, 'Message sent successfully.')

def get_messages(params, rpc_id):
    """
    Получение сообщений.
    """
    token = params.get('token')
    chat_with = params.get('chat_with')

    user_id = validate_session(token)
    if not user_id:
        return error_response(rpc_id, 4, 'Unauthorized.')

    if not chat_with:
        return error_response(rpc_id, 1, 'Chat partner ID is required.')

    conn, cur = db_connect()
    cur.execute("""
        SELECT id, sender_id, receiver_id, text, sent_at
        FROM message
        WHERE 
            ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?))
            AND ((is_deleted_sender = 0 AND sender_id = ?) OR (is_deleted_receiver = 0 AND receiver_id = ?))
        ORDER BY sent_at
    """, (user_id, chat_with, chat_with, user_id, user_id, user_id))
    messages = [
        {
            "id": row["id"],
            "sender_id": row["sender_id"],
            "receiver_id": row["receiver_id"],
            "text": row["text"],
            "sent_at": row["sent_at"]
        }
        for row in cur.fetchall()
    ]
    db_close(conn, cur)

    return success_response(rpc_id, {'messages': messages})

def delete_message(params, rpc_id):
    """
    Удаление сообщения.
    """
    token = params.get('token')
    message_id = params.get('message_id')
    for_sender = params.get('for_sender', False)

    user_id = validate_session(token)
    if not user_id:
        return error_response(rpc_id, 4, 'Unauthorized.')

    if not message_id:
        return error_response(rpc_id, 1, 'Message ID is required.')

    conn, cur = db_connect()
    if for_sender:
        cur.execute(
            "UPDATE message SET is_deleted_sender = 1 WHERE id = ? AND sender_id = ?",
            (message_id, user_id)
        )
    else:
        cur.execute(
            "UPDATE message SET is_deleted_receiver = 1 WHERE id = ? AND receiver_id = ?",
            (message_id, user_id)
        )
    db_close(conn, cur)

    return success_response(rpc_id, 'Message deleted successfully.')

# Вспомогательные функции
def validate_session(token):
    """
    Проверяет валидность сессии.
    """
    conn, cur = db_connect()
    cur.execute("SELECT user_id FROM session WHERE token = ?", (token,))
    session = cur.fetchone()
    db_close(conn, cur)
    return session["user_id"] if session else None

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