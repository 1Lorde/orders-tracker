from flask import Blueprint, request, redirect, url_for, flash, render_template

from orders_tracker.blueprints.devices.service import add_device, update_device
from orders_tracker.forms import NewDeviceForm
from orders_tracker.models import Device

devices_blueprint = Blueprint('devices_bp', __name__, template_folder="templates")


@devices_blueprint.route('/clients/<client_id>/devices/new', methods=['GET', 'POST'])
def new_device(client_id):
    modal_form = NewDeviceForm()

    if request.method == 'POST':
        if modal_form.validate_on_submit():
            created_device = Device(serial=modal_form.serial.data, client_id=client_id, name=modal_form.name.data)
            add_device(created_device)
            return redirect(url_for('clients_bp.client', client_id=created_device.client_id))
        else:
            flash('Пристрій не додано, необхідні поля пусті.', category='warning')

    return render_template('device_modal.html',
                           modal_form=modal_form,
                           message_title="Додавання пристрою",
                           client_id=client_id,
                           color="is-success")


@devices_blueprint.route('/clients/<client_id>/devices/<serial>/edit', methods=['GET', 'POST'])
def edit_device(client_id, serial):
    edited_device = Device.query.filter_by(serial=serial).first()
    modal_form = NewDeviceForm()

    if request.method == 'POST':
        if modal_form.validate_on_submit():
            edited_device.name = modal_form.name.data.strip()
            edited_device.serial = modal_form.serial.data.strip()
            update_device(edited_device)
            return redirect(url_for('clients_bp.client', client_id=edited_device.client_id))
        else:
            flash('Інформацію про пристрій не оновлено, необхідні поля пусті.', category='warning')

    modal_form = NewDeviceForm(edited_device)
    return render_template('device_modal.html',
                           modal_form=modal_form,
                           message_title="Редагування пристрою",
                           client_id=edited_device.client_id,
                           color="is-link")
