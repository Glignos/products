# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, jsonify, request

from .utils import get_products
api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['POST'])
def search():
    count = request.json.get('count')
    radius = request.json.get('radius')
    position = request.json.get('position')
    tags = request.json.get('tags')
    products = get_products(tags, position, radius, count)
    return jsonify({'products': products})



