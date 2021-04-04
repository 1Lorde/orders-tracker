from datetime import datetime

from flask import flash, render_template
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError

from orders_tracker.models import Staff, Order, db


def add_staff(staff):
    try:
        db.session.add(staff)
        db.session.commit()
        flash('Працівника успішно додано.', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Виникла помилка.', category='error')


def get_staff_by_name(name):
    return Staff.query.filter_by(name=name).first()


def get_staff():
    return Staff.query.all()


def get_staff_orders_in_month(staff):
    month = datetime.today().month
    orders_in_month = Order.query.filter_by(staff_id=staff.id).filter(
        extract('month', Order.created_at) == month).count()
    return orders_in_month


def get_staff_orders_in_previous_month(staff):
    prev_month = datetime.today().month - 1
    orders_in_month = Order.query.filter_by(staff_id=staff.id).filter(
        extract('month', Order.created_at) == prev_month).count()
    return orders_in_month


def get_staff_orders_in_year(staff):
    year = datetime.today().year
    orders_in_year = Order.query.filter_by(staff_id=staff.id).filter(
        extract('year', Order.created_at) == year).count()
    return orders_in_year


def render_empty():
    return render_template('staff.html',
                           table='<p class="subtitle is-italic" style="padding:20px;">Нічого не знайдено</p>')
