from flask import Blueprint, render_template, request, redirect, url_for

from orders_tracker.blueprints.staff.service import render_empty, get_staff_stats_in_year
from orders_tracker.forms import NewStaffForm
from orders_tracker.models import Staff
from orders_tracker.blueprints.staff.service import get_staff_stats_in_month, get_staff_stats_in_previous_month, \
    add_staff
from orders_tracker.tables import StaffTable

staff_blueprint = Blueprint('staff_bp', __name__, template_folder="templates")


@staff_blueprint.route('/staff', methods=['GET', 'POST'])
def staff():
    staff_list = Staff.query.all()

    if len(staff_list) == 0:
        return render_empty()

    for worker in staff_list:
        staff_stats = get_staff_stats_in_previous_month(worker)
        setattr(worker, 'stats_prev_month', staff_stats)

        staff_stats = get_staff_stats_in_month(worker)
        setattr(worker, 'stats_month', staff_stats)

        staff_stats = get_staff_stats_in_year(worker)
        setattr(worker, 'stats_year', staff_stats)

    table = StaffTable(staff_list)

    return render_template('staff.html', table=table)


@staff_blueprint.route('/staff/new', methods=['GET', 'POST'])
def new_staff():
    start_page_arg = request.args.get('start')
    modal_form = NewStaffForm()

    if request.method == 'POST' and modal_form.validate_on_submit():
        created_staff = Staff(modal_form.name.data)
        add_staff(created_staff)

        if start_page_arg == '1':
            return redirect(url_for('start_bp.start'))

        return redirect(url_for('staff_bp.staff'))

    if start_page_arg == '1':
        return render_template('new_staff_modal.html',
                               modal_form=modal_form,
                               message_title="Створення нового працівника",
                               return_link=url_for('start_bp.start'))

    return render_template('new_staff_modal.html',
                           modal_form=modal_form,
                           message_title="Створення нового працівника")
