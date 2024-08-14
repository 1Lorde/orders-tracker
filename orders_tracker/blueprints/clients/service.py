import math

from flask import flash, request, render_template
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from orders_tracker.models import Client, db, Device


def search_in_columns(search, query):
    condition = or_(Client.name.ilike(f"%{search}%"),
                    Client.phone.ilike(f"%{search}%"),
                    Client.address.ilike(f"%{search}%"),
                    Client.notes.ilike(f"%{search}%"), )
    return query.filter(condition)


def search_clients(search_string):
    clients_query = Client.query

    if not search_string:
        return clients_query

    search_queries = search_string.split(' ')
    for search_query in search_queries:
        clients_query = search_in_columns(search_query, clients_query)
    return clients_query


def paginate_clients(metadata, clients_query):
    clients_query = clients_query.paginate(page=metadata['current'], per_page=metadata['rows_per_page'])

    return clients_query.items


def get_pagination_metadata(page, clients_query):
    rows_per_page = 8
    last_page = math.ceil(clients_query.count() / rows_per_page)

    return {'current': page, 'next': page + 1, 'previous': page - 1,
            'first': 1, 'last': last_page, 'rows_per_page': rows_per_page}


def get_path_args():
    return request.args.get('search_query'), \
           request.args.get('page', 1, type=int)


def render_empty(stats, search_arg):
    return render_template('clients.html',
                           table='<p class="subtitle is-italic" style="padding:20px;">Нічого не знайдено</p>',
                           stats=stats,
                           search_field_value=search_arg,
                           pagination_data=None)


def get_form_fields():
    search_field = request.form['search_field'] if request.form['search_field'] else None
    return search_field


def add_client(client):
    db.session.add(client)
    try:
        db.session.commit()
        flash('Клієнта успішно додано.', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Клієнт з таким номером телефону або ім\'ям вже існує.', category='error')


def update_client(client):
    try:
        db.session.merge(client)
        db.session.commit()
        flash('Інформацію оновлено.', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('При оновленні інформації про клієнта виникла помилка.', category='error')


def remove_client(client):
    try:
        db.session.query(Device).filter(Device.client_id == client.id).delete()
        db.session.delete(client)
        db.session.commit()
        flash('Клієнта видалено.', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Клієнта неможливо видалити, оскільки існують пов\'язані з ним замовлення.', category='error')


def client_exists(name):
    return Client.query.filter_by(name=name).first() is not None


def get_client_by_name(name):
    return Client.query.filter_by(name=name).first()


def get_clients_count():
    return Client.query.count()
