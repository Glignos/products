from flask import Blueprint, current_app, jsonify, render_template

views = Blueprint('/', __name__)


@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')
