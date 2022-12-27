from flask import abort, flash, redirect, render_template

from . import BASE_URL, app, db
from .forms import LinkForm
from .models import URLMap
from .utils import check_allowed_symbols, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        original = form.original_link.data

        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Имя {} уже занято!'.format(custom_id))
            return render_template('main.html', form=form)
        if custom_id is not None and not check_allowed_symbols(custom_id):
            flash('Указан недопустимый символ в короткой ссылке. '
                  'Достпустимые символы: A-z, 0-9.')
            return render_template('main.html', form=form)
        if custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()

        urlMap = URLMap(
            original=original,
            short=custom_id,
        )
        db.session.add(urlMap)
        db.session.commit()
        return render_template('main.html', form=form, short_link=BASE_URL + urlMap.short,
                               original_link=urlMap.original)
    return render_template('main.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_to(short):
    url = URLMap.query.filter_by(short=short).first()
    if url:
        return redirect(url.original)
    abort(404)