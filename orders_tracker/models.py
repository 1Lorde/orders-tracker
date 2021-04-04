from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    phone = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(200))
    notes = db.Column(db.String(1000))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, phone=None, address=None, notes=None):
        self.name = name
        self.phone = phone
        self.address = address
        self.notes = notes

    def __repr__(self):
        return self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float)

    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'), nullable=False)
    status = db.relationship('OrderStatus', backref=db.backref('templates', lazy=True))

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('templates', lazy=True))

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('templates', lazy=True))

    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    staff = db.relationship('Staff', backref=db.backref('templates', lazy=True))

    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, client_id=None, device_id=None,
                 staff_id=None, description=None, price=None, created_at=None, status_id=None):
        self.title = title
        self.description = description
        self.price = price
        self.client_id = client_id
        self.device_id = device_id
        self.staff_id = staff_id
        self.created_at = created_at
        self.status_id = status_id

    def __repr__(self):
        return '<Order %r>' % self.title


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    serial = db.Column(db.String(200), nullable=False, unique=True)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('devices', lazy=True))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, serial, client_id, name=None):
        self.name = name
        self.serial = serial
        self.client_id = client_id

    def __repr__(self):
        return self.serial


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class OrderStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
