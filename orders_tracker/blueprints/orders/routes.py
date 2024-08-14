from flask import Blueprint, request, render_template, redirect, url_for, flash

from orders_tracker.forms import NewOrderForm, NavigationForm, CancelConfirmForm
from orders_tracker.models import Order, Staff
from orders_tracker.blueprints.orders.service import add_order, get_orders_count, get_form_fields, get_path_args, \
    filter_orders, \
    render_empty, paginate_orders, get_pagination_metadata, update_order
from orders_tracker.tables import OrdersTable

orders_blueprint = Blueprint('orders_bp', __name__, template_folder="templates")


@orders_blueprint.route('/orders/new', methods=['GET', 'POST'])
def new_order():
    choices = Staff.query.all()
    form = NewOrderForm(formdata=request.form, staff_choices=choices)
    if request.method == 'POST':
        if form.validate_on_submit():
            return_code = add_order(form)
            if return_code == 0:
                return redirect(url_for('orders_bp.orders'))
        else:
            flash('Перевірте введені значення.', category='warning')

    return render_template('new_order.html', form=form)


@orders_blueprint.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        sort_by_field, status_field, search_field = get_form_fields()
        return redirect(url_for('orders_bp.orders',
                                sort_by=sort_by_field,
                                status=status_field,
                                search_query=search_field))

    search_arg, sort_by_arg, status_arg, page_arg = get_path_args()

    stats = {'total': get_orders_count(), 'filter': -1}

    orders_query = filter_orders(search_arg, sort_by_arg, status_arg)

    navigation_form = NavigationForm(search_field=search_arg,
                                     sort_by_field=sort_by_arg,
                                     status_field=status_arg)

    stats['filter'] = orders_query.count()
    if stats['filter'] == 0:
        return render_empty(stats, navigation_form)

    pagination_metadata = get_pagination_metadata(page_arg, orders_query)
    orders_list = paginate_orders(pagination_metadata, orders_query)
    table = OrdersTable(orders_list)

    return render_template('orders.html',
                           table=table,
                           stats=stats,
                           pagination_data=pagination_metadata,
                           navigation_form=navigation_form)


@orders_blueprint.route('/orders/<order_id>', methods=['GET', 'POST'])
def order(order_id):
    selected_order = Order.query.filter_by(id=order_id).first_or_404()

    if request.method == 'POST':
        if request.form.get('start'):
            selected_order.status_id = 2
        elif request.form.get('finish'):
            selected_order.status_id = 3

        update_order(selected_order)
        return redirect(url_for('orders_bp.order', order_id=selected_order.id))

    return render_template('order.html', order=selected_order)


@orders_blueprint.route('/orders/<order_id>/cancel', methods=['GET', 'POST'])
def cancel_order(order_id):
    selected_order = Order.query.filter_by(id=order_id).first_or_404()
    form = CancelConfirmForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            selected_order.status_id = 4
            update_order(selected_order)
            return redirect(url_for('orders_bp.order', order_id=selected_order.id))

    return render_template('cancel_confirm.html',
                           form=form,
                           order_id=selected_order.id,
                           message_title="Скасування замовлення",
                           message="Ви дійсно бажаєте скасувати замовлення №" + str(selected_order.id) + "?")
