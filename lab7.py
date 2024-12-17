from flask import Blueprint, render_template, abort, Response, request
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

def make_json_response(data, status_code=200):
    """Функция для создания JSON-ответа вручную"""
    response = Response(json.dumps(data, ensure_ascii=False), status=status_code, mimetype='application/json')
    return response

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Возвращает весь список фильмов"""
    return make_json_response(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film_by_id(id):
    """Возвращает фильм по ID с проверкой диапазона"""
    if 0 <= id < len(films):
        return make_json_response(films[id])
    else:
        abort(404, description="Фильм с указанным ID не найден")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удаляет фильм по ID с проверкой диапазона"""
    if 0 <= id < len(films):
        deleted_film = films.pop(id)
        return make_json_response({"message": f"Фильм '{deleted_film['title']}' успешно удален"})
    else:
        abort(404, description="Фильм с указанным ID не найден")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновляет информацию о фильме по ID с проверкой диапазона"""
    if 0 <= id < len(films):
        film = request.get_json()

        # Проверка описания
        if not film.get('description'):
            return make_json_response({"description": "Описание фильма не может быть пустым"}, 400)

        # Проверка на обязательные поля
        required_fields = ["title", "title_ru", "year", "description"]
        if not all(field in film for field in required_fields):
            return make_json_response({"error": "Отсутствуют обязательные поля"}, 400)

        films[id] = film  # Обновление фильма
        return make_json_response(films[id], status_code=200)
    else:
        abort(404, description="Фильм с указанным ID не найден")

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавляет новый фильм с проверкой на пустые поля"""
    new_film = request.get_json()

    # Проверка на пустые данные
    if not new_film:
        return make_json_response({"error": "Данные для добавления не предоставлены"}, 400)

    # Проверка на обязательные поля
    required_fields = ["title", "title_ru", "year", "description"]
    if not all(field in new_film for field in required_fields):
        return make_json_response({"error": "Отсутствуют обязательные поля"}, 400)

    # Проверка описания
    if not new_film.get('description'):
        return make_json_response({"description": "Описание фильма не может быть пустым"}, 400)

    # Добавление фильма в список
    films.append(new_film)
    new_index = len(films) - 1  # Индекс нового элемента

    return make_json_response({"index": new_index}, status_code=201)
