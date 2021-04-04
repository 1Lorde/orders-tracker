from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, render_template, redirect, url_for
from flask_datepicker import datepicker
from sqlalchemy_utils import database_exists

from orders_tracker.api.api import api_blueprint
from orders_tracker.blueprints.clients.routes import clients_blueprint
from orders_tracker.blueprints.devices.routes import devices_blueprint
from orders_tracker.blueprints.start.routes import start_blueprint
from orders_tracker.models import db, OrderStatus, Staff, Client
from orders_tracker.blueprints.orders.routes import orders_blueprint
from orders_tracker.blueprints.staff.routes import staff_blueprint


def init_db(flask_app):
    db.init_app(flask_app)
    db.create_all()

    new = OrderStatus("Нове")
    in_process = OrderStatus("В процесі")
    done = OrderStatus("Виконано")
    cancelled = OrderStatus("Скасовано")
    db.session.add(new)
    db.session.add(in_process)
    db.session.add(done)
    db.session.add(cancelled)
    db.session.commit()


app = Flask(__name__, template_folder='templates')
app.register_blueprint(orders_blueprint)
app.register_blueprint(clients_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(staff_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(start_blueprint)

Path(Path.home(), Path('orders-tracker')).mkdir(parents=True, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{str(Path.home())}/orders-tracker/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ajasdjfklsdhasudh238yunf823yremfi7T^&%&*'

db.init_app(app)
datepicker(app=app, local=['static/js/jquery-ui.js', 'static/jquery-ui.css'])

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    with app.test_request_context():
        init_db(app)


@app.context_processor
def get_last_week():
    today = datetime.today()
    week = timedelta(days=7)
    week_earlier = today - week

    return dict(week=f"{week_earlier.strftime('%d.%m.%y')}-{today.strftime('%d.%m.%y')}")


@app.context_processor
def get_last_month():
    today = datetime.today()
    month = timedelta(days=30)
    month_earlier = today - month

    return dict(month=f"{month_earlier.strftime('%d.%m.%y')}-{today.strftime('%d.%m.%y')}")


@app.route('/')
def index():
    if Staff.query.count() == 0 or Client.query.count() == 0:
        return redirect(url_for("start_bp.start"))
    else:
        return redirect(url_for("orders_bp.orders"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    app.run()
