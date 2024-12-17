from flask import Blueprint, render_template, abort, Response
import json

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# Список фильмов
films = [
    {
        "title": "Venom",
        "title_ru": "Веном",
        "year": 2018,
        "description": "История о репортере Эдди Броке, который становится хозяином инопланетного симбиота Венома. "
                    "Теперь он обретает сверхчеловеческие способности и вынужден сражаться как герой, несмотря на мрачную сущность Венома."
    },
    {
        "title": "Breaking Bad",
        "title_ru": "Во все тяжкие",
        "year": 2008,
        "description": "Сюжет рассказывает о школьном учителе химии Уолтере Уайте, который, узнав о смертельной болезни, "
                    "начинает варить метамфетамин, чтобы обеспечить семью после своей смерти. История о выборе, морали и последствиях."
    },
    {
        "title": "The Pursuit of Happyness",
        "title_ru": "В погоне за счастьем",
        "year": 2006,
        "description": "Трогательная история о Крисе Гарднере, который, несмотря на трудности и бездомность, "
                    "пытается обеспечить достойное будущее своему сыну. Основано на реальных событиях."
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
        abort(404)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удаляет фильм по ID с проверкой диапазона"""
    if 0 <= id < len(films):
        deleted_film = films.pop(id)
        return make_json_response({"message": f"Фильм '{deleted_film['title']}' успешно удален"})
    else:
        abort(404)
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновляет информацию о фильме по ID с проверкой диапазона"""
    if 0 <= id < len(films):  # Проверка на корректность ID
        film = request.get_json()
        if not film:  # Проверка на наличие данных
            abort(400, "Данные для обновления не предоставлены")

        films[id] = film  # Обновление фильма
        return make_json_response(films[id], status_code=200)
    else:
        abort(404, "Фильм с указанным ID не найден")  