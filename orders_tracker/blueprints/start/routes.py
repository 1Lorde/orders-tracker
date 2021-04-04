from flask import Blueprint, render_template

start_blueprint = Blueprint('start_bp', __name__, template_folder="templates")


@start_blueprint.route('/start', methods=['GET'])
def start():
    return render_template('start_base.html')
