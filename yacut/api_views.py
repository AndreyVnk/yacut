from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_allowed_symbols, get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)


@app.route('/api/id/', methods=['POST'])
def modify_url_to_short():

    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)

    if 'url' not in data or data['url'] == '':
        raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)

    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    if len(data['custom_id']) > 16 or not check_allowed_symbols(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Имя "{}" уже занято.'.format(data['custom_id']), 400)

    urlMap = URLMap()
    urlMap.from_dict(data)
    db.session.add(urlMap)
    db.session.commit()
    return jsonify(urlMap.to_dict()), 201
