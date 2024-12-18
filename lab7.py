from flask import Blueprint, render_template, abort, Response, request
from datetime import datetime
import json

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

# Список фильмов
films = [
    {
        "title": "Venom",
        "title_ru": "Веном",
        "year": 2018,
        "description": "История о репортере Эдди Броке, который становится хозяином инопланетного симбиота Венома."
    },
    {
        "title": "Breaking Bad",
        "title_ru": "Во все тяжкие",
        "year": 2008,
        "description": "Сюжет рассказывает о школьном учителе химии Уолтере Уайте, который начинает варить метамфетамин."
    },
    {
        "title": "The Pursuit of Happyness",
        "title_ru": "В погоне за счастьем",
        "year": 2006,
        "description": "Трогательная история о Крисе Гарднере, который пытается обеспечить будущее своему сыну."
    }
]

# Функция для создания JSON-ответов
def make_json_response(data, status_code=200):
    response = Response(json.dumps(data, ensure_ascii=False), status=status_code, mimetype='application/json')
    return response

# Функция валидации данных фильма
def validate_film(data):
    errors = {}
    current_year = datetime.now().year  # Текущий год

    # Проверка на наличие русскоязычного названия
    if not data.get('title_ru') or not data['title_ru'].strip():
        errors['title_ru'] = "Русское название не может быть пустым."

    # Проверка оригинального названия
    if not data.get('title') or not data['title'].strip():
        if not data.get('title_ru') or not data['title_ru'].strip():
            errors['title'] = "Название на оригинальном языке не может быть пустым, если русское название отсутствует."

    # Проверка года выпуска
    if 'year' not in data or not isinstance(data['year'], int):
        errors['year'] = "Год выпуска должен быть числом."
    elif data['year'] < 1895 or data['year'] > current_year:
        errors['year'] = f"Год выпуска должен быть от 1895 до {current_year}."

    # Проверка описания
    if not data.get('description') or not data['description'].strip():
        errors['description'] = "Описание не может быть пустым."
    elif len(data['description']) > 2000:
        errors['description'] = "Описание не может превышать 2000 символов."

    return errors

# Маршрут для получения всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return make_json_response(films)

# Маршрут для получения фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film_by_id(id):
    if 0 <= id < len(films):
        return make_json_response(films[id])
    abort(404, description="Фильм с указанным ID не найден.")

# Маршрут для удаления фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        deleted_film = films.pop(id)
        return make_json_response({"message": f"Фильм '{deleted_film['title']}' успешно удален."})
    abort(404, description="Фильм с указанным ID не найден.")

# Маршрут для обновления фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        data = request.get_json()
        errors = validate_film(data)
        if errors:
            return make_json_response(errors, 400)

        films[id] = data
        return make_json_response(films[id])
    abort(404, description="Фильм с указанным ID не найден.")

# Маршрут для добавления нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    errors = validate_film(data)
    if errors:
        return make_json_response(errors, 400)

    films.append(data)
    new_index = len(films) - 1
    return make_json_response({"index": new_index}, 201)