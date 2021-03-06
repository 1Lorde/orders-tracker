import math
import re
from datetime import datetime

from flask import flash, request, render_template
from sqlalchemy import or_, extract
from sqlalchemy.exc import IntegrityError

from orders_tracker.blueprints.clients.service import client_exists, get_client_by_name, add_client
from orders_tracker.blueprints.devices.service import device_exists, get_device_by_serial, add_device
from orders_tracker.blueprints.staff.service import get_staff_by_name
from orders_tracker.models import db, Order, Client, Device, Staff, OrderStatus, OrderType

date_pattern = re.compile(r'^(\d{1,2}\.\d{1,2}\.\d{2,4})$')
day_pattern = re.compile(r'^(\d{1,2})$')
day_month_pattern = re.compile(r'^(\d+\.\d+)$')
dd_pattern = re.compile(r'^(\d{1,2}.\d{1,2}\.\d{2,4}\-\d{1,2}\.\d{1,2}\.\d{2,4})$')


def search_in_columns(search, query):
    condition = or_(Order.description.ilike(f"%{search}%"),
                    Order.client.has(Client.name.ilike(f"%{search}%")),
                    Order.device.has(Device.serial.ilike(f"%{search}%")),
                    Order.staff.has(Staff.name.ilike(f"%{search}%")))
    return query.filter(condition)


def is_date_filter(search_query):
    if dd_pattern.search(search_query) or date_pattern.search(search_query) or \
            day_pattern.search(search_query) or day_month_pattern.search(search_query):
        return True
    return False


def try_parsing_date(text):
    for fmt in ('%d.%m.%Y', '%d.%m.%y', '%d.%m'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    flash('Некоректний пошуковий запит.', category='error')


def date_search(search_query, orders_query):
    if dd_pattern.search(search_query):
        dates = dd_pattern.search(search_query).group(0).split("-")
        date1 = try_parsing_date(dates[0])
        date2 = try_parsing_date(dates[1])
        if date1 and date2:
            orders_query = orders_query.filter(Order.created_at >= date1) \
                .filter(Order.created_at <= date2)

    elif date_pattern.search(search_query):
        date = try_parsing_date(date_pattern.search(search_query).group(0))
        if date:
            orders_query = orders_query.filter(Order.created_at == date)

    elif day_pattern.search(search_query):
        day = day_pattern.search(search_query).group(0)
        if day:
            orders_query = orders_query.filter(extract('day', Order.created_at) == day)

    elif day_month_pattern.search(search_query):
        date = try_parsing_date(day_month_pattern.search(search_query).group(0))
        if date:
            orders_query = orders_query.filter(extract('day', Order.created_at) == date.day) \
                .filter(extract('month', Order.created_at) == date.month)

    return orders_query


def search_orders(search_string, orders_query):
    if not search_string:
        return orders_query

    search_queries = search_string.split(' ')
    for search_query in search_queries:
        if is_date_filter(search_query):
            orders_query = date_search(search_query, orders_query)
        else:
            orders_query = search_in_columns(search_query, orders_query)
    return orders_query


def sort_orders(sort_by, orders_query):
    if not sort_by:
        return orders_query

    orders_query = orders_query.order_by(None)

    if sort_by == 'new_first':
        orders_query = orders_query.order_by(Order.created_at.desc())
    elif sort_by == 'old_first':
        orders_query = orders_query.order_by(Order.created_at)
    elif sort_by == 'client':
        orders_query = orders_query.order_by(Order.client_id)
    elif sort_by == 'status':
        orders_query = orders_query.order_by(Order.status_id)
    return orders_query


def filter_by_status(status, orders_query):
    if not status or status == '0':
        return orders_query

    orders_query = orders_query.filter(Order.status_id == int(status))
    return orders_query


def filter_by_type(order_type, orders_query):
    if not order_type or order_type == '0':
        return orders_query

    orders_query = orders_query.filter(Order.type_id == int(order_type))
    return orders_query


def paginate_orders(metadata, orders_query):
    orders_query = orders_query.paginate(page=metadata['current'], per_page=metadata['rows_per_page'])

    return orders_query.items


def get_pagination_metadata(page, orders_query):
    rows_per_page = 8
    last_page = math.ceil(orders_query.count() / rows_per_page)

    return {'current': page, 'next': page + 1, 'previous': page - 1,
            'first': 1, 'last': last_page, 'rows_per_page': rows_per_page}


def filter_orders(search, sort_by, status, order_type):
    orders_query = Order.query.order_by(Order.created_at.desc())
    orders_query = search_orders(search, orders_query)
    orders_query = sort_orders(sort_by, orders_query)
    orders_query = filter_by_status(status, orders_query)
    orders_query = filter_by_type(order_type, orders_query)
    return orders_query


def get_path_args():
    return request.args.get('search_query'), \
           request.args.get('sort_by'), \
           request.args.get('status'), \
           request.args.get('type'), \
           request.args.get('page', 1, type=int)


def get_form_fields():
    sort_by_field = request.form['sort_by_field'] if request.form['sort_by_field'] != 'new_first' else None
    status_field = request.form['status_field'] if request.form['status_field'] != '0' else None
    type_field = request.form['type_field'] if request.form['type_field'] != '0' else None
    search_field = request.form['search_field'] if request.form['search_field'] else None
    return sort_by_field, status_field, type_field, search_field


def render_empty(stats, navigation_form):
    return render_template('orders.html',
                           table='<p class="subtitle is-italic" style="padding:20px;">Нічого не знайдено</p>',
                           stats=stats,
                           pagination_data=None, navigation_form=navigation_form)


def add_order(form):
    if client_exists(form.client.data):
        client = get_client_by_name(form.client.data)
    else:
        client = Client(form.client.data)
        add_client(client)

    if device_exists(form.serial.data, client.id):
        device = get_device_by_serial(form.serial.data, client.id)
    else:
        device = Device(form.serial.data, client.id)
        add_device(device)

    staff = get_staff_by_name(form.staff.data)
    order_type = get_order_type_by_name(form.type.data)

    order = Order(description=form.description.data,
                  client_id=client.id,
                  device_id=device.id,
                  staff_id=staff.id,
                  price=form.price.data,
                  status_id=1,
                  type_id=order_type.id,
                  created_at=datetime.strptime(form.created_at.data, "%d.%m.%Y"))

    try:
        db.session.add(order)
        db.session.commit()
        flash('Замовлення успішно додано.', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Виникла помилка.', category='error')


def update_order(form, order_id):
    if client_exists(form.client.data):
        client = get_client_by_name(form.client.data)
    else:
        client = Client(form.client.data)
        add_client(client)

    if device_exists(form.serial.data, client.id):
        device = get_device_by_serial(form.serial.data, client.id)
    else:
        device = Device(form.serial.data, client.id)
        add_device(device)

    staff = get_staff_by_name(form.staff.data)
    order_type = get_order_type_by_name(form.type.data)

    edited_order = Order.query.filter_by(id=order_id).first()
    edited_order.client_id = client.id
    edited_order.device_id = device.id
    edited_order.description = form.description.data
    edited_order.staff_id = staff.id
    edited_order.price = form.price.data
    edited_order.created_at = datetime.strptime(form.created_at.data, "%d.%m.%Y")
    edited_order.type_id = order_type.id

    try:
        db.session.merge(edited_order)
        db.session.commit()
        flash('Інформацію оновлено.', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('При оновленні інформації про замовлення виникла помилка.', category='error')


def get_orders_count():
    return Order.query.count()


def get_order_type_by_name(name):
    return OrderType.query.filter_by(name=name).first()


def get_order_statuses_choices():
    statuses = OrderStatus.query.all()
    statuses.insert(0, 'Всі')
    it = iter(statuses)
    statuses_dict = dict(zip(range(len(statuses)), it))
    status_choices = []
    for key, value in statuses_dict.items():
        temp = [key, value]
        status_choices.append(temp)
    return status_choices


def get_order_types_choices():
    types = OrderType.query.all()
    types.insert(0, 'Всі')
    it = iter(types)
    types_dict = dict(zip(range(len(types)), it))
    types_choices = []
    for key, value in types_dict.items():
        temp = [key, value]
        types_choices.append(temp)
    return types_choices
