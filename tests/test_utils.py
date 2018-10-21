from server.utils import convert_tags_to_ids, filter_with_tags, filter_with_radius, calculate_distance, get_popular_products
import math
import pytest
import os
from csv import DictReader, reader

stores_file = '../data/shops.csv' # Maybe move them in a general config could be an overkill in this case
dir = os.path.dirname(__file__)

@pytest.mark.parametrize("test_input,expected", [
    (["trousers","plates"], ["b4a59f0e2e1342efa451237125bb331a","805ea814c22f4750ad1ede82e9eaad83"]),
    (["women","kids"], ["4a6cf7ee90f74f12869e8bdbc90398b9","146f3cc1b95e41fb9b7a1fc94544d961"])
])
def test_tag_conversion_to_ids(test_input, expected):
    assert convert_tags_to_ids(test_input) == expected


def test_filter_radius():
    with open(os.path.join(dir,stores_file), 'r') as file:
     stores = [i for i in DictReader(file, delimiter=',')]
    customer_position = {'lat': 59.33265172650577, 'lng': 18.01061237898399}
    filtered_stores = filter_with_radius(customer_position, stores, 5.6)
    assert filtered_stores[0] == '4aa53e646bf84faca9a76c020b0682de'


def test_calculate_distance():
    assert  calculate_distance(18.01061237898399, 59.33265172650577, 18.06061237898499, 59.33265972650577) == 5.534039829204032


def test_filter_with_tags():
    tags = ['clothes']
    stores = ['4aa53e646bf84faca9a76c020b0682de', 'cc0b3a06381b43df8064f179adc60978']
    filtered_shops = filter_with_tags(tags, stores)
    assert filtered_shops == ['4aa53e646bf84faca9a76c020b0682de']


def test_get_popular_products():
    shops = ['4aa53e646bf84faca9a76c020b0682de', '6c071e36fe5549fe804fc39e676c438d', '42a998ead8ed4694b04bfd72cd1083fe']
    test_products = [{'popularity': 11.866, 'product_title': 'Nike air royalty'},
     {'popularity': 8.379999999999999, 'product_title': 'Private Listing #2'},
      {'popularity': 7.029, 'product_title': 'TAKLAMPA VIT 60 CM ECO'}, {'popularity': 6.041, 'product_title': 'Ipad Sleeve brown'}, {'popularity': 5.432, 'product_title': 'Raw Choc Brownie'}]

    assert get_popular_products(shops, 5) == test_products



