from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

RGZ = Blueprint('RGZ', __name__)

# Инициализация базы данных
db = SQLAlchemy()

# Модели базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Роуты
@RGZ.route('/welcome/')
def welcome():
    """
    Приветственная страница.
    """
    return {
        'message': 'Welcome to the Messenger API. Please register or login.',
        'instructions': 'Use /json-rpc-api/ endpoint for API calls.'
    }

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
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': rpc_id
        }

# Функции API
def register_user(params, rpc_id):
    """
    Регистрация пользователя.
    """
    username = params.get('username')
    password = params.get('password')

    if not username or not password:
        return error_response(rpc_id, 1, 'Username and password are required.')

    if User.query.filter_by(username=username).first():
        return error_response(rpc_id, 2, 'Username already exists.')

    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return success_response(rpc_id, 'User registered successfully.')

def login_user(params, rpc_id):
    """
    Авторизация пользователя.
    """
    username = params.get('username')
    password = params.get('password')

    if not username or not password:
        return error_response(rpc_id, 1, 'Username and password are required.')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return error_response(rpc_id, 3, 'Invalid username or password.')

    session_token = generate_password_hash(f"{username}{datetime.utcnow()}")
    new_session = Session(token=session_token, user_id=user.id)
    db.session.add(new_session)
    db.session.commit()

    return success_response(rpc_id, {'token': session_token})

def get_users(params, rpc_id):
    """
    Получение списка пользователей.
    """
    token = params.get('token')

    if not token or not validate_session(token):
        return error_response(rpc_id, 4, 'Unauthorized.')

    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return success_response(rpc_id, {'users': user_list})

# Вспомогательные функции
def validate_session(token):
    """
    Проверяет валидность сессии.
    """
    session = Session.query.filter_by(token=token).first()
    return session is not None

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