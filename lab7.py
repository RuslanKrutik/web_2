from flask import Blueprint, render_template, jsonify, abort

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

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

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Возвращает весь список фильмов"""
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film_by_id(id):
    """Возвращает фильм по ID с проверкой диапазона"""
    if 0 <= id < len(films):  # Проверка на корректность ID
        return jsonify(films[id])
    else:
        abort(404)  # Возвращает 404, если ID некорректный
