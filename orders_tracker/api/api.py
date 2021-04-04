import json

from flask import Blueprint, Response, request

from orders_tracker.models import Client, Device, OrderStatus, Staff

api_blueprint = Blueprint('api_bp', __name__)


@api_blueprint.route('/api/autocomplete/clients', methods=['GET'])
def client_autocomplete():
    clients = [obj[0] for obj in Client.query.with_entities(Client.name).all()]

    return Response(json.dumps(clients), mimetype='application/json')


@api_blueprint.route('/api/autocomplete/devices', methods=['GET'])
def serial_autocomplete():
    client_name = request.args.get('client_name')
    client_id = Client.query.filter_by(name=client_name).with_entities(Client.id).first()
    if client_id is not None:
        serials = [obj[0] for obj in Device.query.filter_by(client_id=client_id[0]).with_entities(Device.serial).all()]

        return Response(json.dumps(serials), mimetype='application/json')
    return Response(status=404)


@api_blueprint.route('/api/autocomplete/staff', methods=['GET'])
def staff_autocomplete():
    staff = [obj[0] for obj in Staff.query.with_entities(Staff.name).all()]

    return Response(json.dumps(staff), mimetype='application/json')


@api_blueprint.route('/api/order_status/<status_id>', methods=['GET'])
def order_status(status_id):
    status_name = OrderStatus.query.filter_by(id=status_id).with_entities(OrderStatus.name).first()[0]

    return status_name
