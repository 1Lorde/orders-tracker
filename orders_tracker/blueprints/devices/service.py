from flask import flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from orders_tracker.models import db, Device


def add_device(device):
    db.session.add(device)
    try:
        db.session.commit()
        flash('Пристрій успішно додано.', category='success')
        return redirect(url_for('clients_bp.client', client_id=device.client_id))
    except IntegrityError:
        db.session.rollback()
        flash('Пристрій з таким серійним номером вже існує.', category='error')


def update_device(device):
    try:
        db.session.merge(device)
        db.session.commit()
        flash('Інформацію оновлено.', category='success')
        return redirect(url_for('clients_bp.client', client_id=device.client_id))
    except IntegrityError:
        db.session.rollback()
        flash('При оновленні інформації про пристрій виникла помилка.', category='error')


def device_exists_by_serial(serial):
    return Device.query.filter_by(serial=serial).first() is not None


def get_device_by_serial(serial):
    return Device.query.filter_by(serial=serial).first()
