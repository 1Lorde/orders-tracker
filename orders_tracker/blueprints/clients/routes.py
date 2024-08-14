import urllib

from flask import Blueprint, request, render_template, flash, redirect, url_for

from orders_tracker.blueprints.clients.service import add_client, update_client, remove_client, search_clients, \
    get_form_fields, get_path_args, \
    get_clients_count, render_empty, get_pagination_metadata, paginate_clients
from orders_tracker.forms import NewClientForm, DeleteConfirmForm
from orders_tracker.models import Client, Device
from orders_tracker.tables import ClientsTable

clients_blueprint = Blueprint('clients_bp', __name__, template_folder="templates")


@clients_blueprint.route('/clients/new', methods=['GET', 'POST'])
def new_client():
    form = NewClientForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            created_client = Client(form.name.data, form.phone.data, form.address.data, form.notes.data)
            add_client(created_client)
            return redirect(url_for('clients_bp.clients'))
        else:
            flash('Перевірте введені значення.', category='warning')

    return render_template('new_client.html', form=form)


@clients_blueprint.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        search_field = get_form_fields()
        return redirect(url_for('clients_bp.clients',
                                search_query=search_field))

    search_arg, page_arg = get_path_args()

    stats = {'total': get_clients_count(), 'filter': -1}

    clients_query = search_clients(search_arg)

    stats['filter'] = clients_query.count()
    if stats['filter'] == 0:
        return render_empty(stats, search_arg)

    pagination_metadata = get_pagination_metadata(page_arg, clients_query)

    clients_list = paginate_clients(pagination_metadata, clients_query)
    table = ClientsTable(clients_list)

    return render_template('clients.html',
                           table=table,
                           stats=stats,
                           search_field_value=search_arg,
                           pagination_data=pagination_metadata)


@clients_blueprint.route('/clients/<client_id>', methods=['GET', 'POST'])
def client(client_id):
    address_link = None
    selected_client = Client.query.filter_by(id=client_id).first_or_404()
    if selected_client.address:
        address_link = "https://www.google.com/maps/search/?api=1&query=" + \
                       urllib.parse.quote_plus(selected_client.address)

    devices = Device.query.filter_by(client_id=client_id).all()

    return render_template('client.html',
                           client=selected_client,
                           devices=devices,
                           address_link=address_link)


@clients_blueprint.route('/clients/<client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    edited_client = Client.query.filter_by(id=client_id).first()
    modal_form = NewClientForm()

    if request.method == 'POST':
        if modal_form.validate_on_submit():
            edited_client.name = modal_form.name.data.strip()
            edited_client.phone = modal_form.phone.data
            edited_client.address = modal_form.address.data
            edited_client.notes = modal_form.notes.data
            update_client(edited_client)
            return redirect(url_for('clients_bp.client', client_id=edited_client.id))
        else:
            flash('Дані про клієнта не оновлено.', category='warning')

    modal_form = NewClientForm(edited_client)
    return render_template('edit_client.html',
                           form=modal_form,
                           message_title="Редагування інформації про клієнта",
                           client_id=edited_client.id,
                           color="is-link")


@clients_blueprint.route('/clients/<client_id>/delete', methods=['GET', 'POST'])
def delete_client(client_id):
    deleted_client = Client.query.filter_by(id=client_id).first()
    form = DeleteConfirmForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            remove_client(deleted_client)
            return redirect(url_for('clients_bp.clients'))

    return render_template('delete_confirm.html',
                           form=form,
                           client_id=deleted_client.id,
                           message_title="Видалення клієнта",
                           message="Ви дійсно бажаєте видалити клієнта " + deleted_client.name + "?")
