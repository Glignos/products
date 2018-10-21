from csv import DictReader, reader
import os
from math import cos, asin, sqrt
import operator

import geopy.distance

dir = os.path.dirname(__file__)


shops_file = '../data/shops.csv' # Maybe move them in a general config could be an overkill in this case
tags_file = '../data/tags.csv'
shop_taggings_file = '../data/taggings.csv'
products_file = '../data/products.csv'

def get_products(tags, customer_position, radius, products_num):
    with open(os.path.join(dir,shops_file), 'r') as file:
        shops = [i for i in DictReader(file, delimiter=',')]
    shops_filtered_by_radius = filter_with_radius(customer_position, shops, radius)
    shops_filtered_by_tags = filter_with_tags(tags, shops_filtered_by_radius)
    return get_popular_products(shops_filtered_by_tags, products_num)
    

def filter_with_radius(customer_position, shops, radius):
    customer_lat = float(customer_position['lat'])
    customer_long = float(customer_position['lng'])
    filtered_rows = []
    for row in shops:
        if(calculate_distance(customer_lat, customer_long, float(row['lat']), float(row['lng'])) < radius):
            filtered_rows.append(row['id'])
    return filtered_rows


def calculate_distance(customer_lat,customer_lon, store_lat, store_lon):
    customer_coord = (customer_lat, customer_lon)
    store_coord = (store_lat, store_lon)
    return geopy.distance.vincenty(customer_coord, store_coord).km

def filter_with_tags(tags, available_shops):
    shops_with_matching_tags = []
    if not tags:
        return available_shops
    tags_ids = convert_tags_to_ids(tags)
    with open(os.path.join(dir,shop_taggings_file), 'r') as file:
        shops_taggings = [i for i in DictReader(file, delimiter=',')]

    for row in shops_taggings:
        if row['tag_id'] in tags_ids:
            shops_with_matching_tags.append(row['shop_id'])
    return list(frozenset(available_shops).intersection(frozenset(shops_with_matching_tags))) # we compare the allready filtered by
    # radius shops with the ones that match our taggings

def convert_tags_to_ids(tags):
    ids = []
    with open(os.path.join(dir,tags_file), 'r') as file:
     shops = [i for i in DictReader(file, delimiter=',')]
    
    for row in shops:
        if row['tag'] in tags:
            ids.append(row['id'])
    return ids


def get_popular_products(shops, products_num):
    counted_products = {}
    with open(os.path.join(dir,products_file), 'r') as file:
        products = [i for i in DictReader(file, delimiter=',')]   
    shops = frozenset(shops)
    for row in products:
        if row['shop_id'] in shops:
            if counted_products.get(row['title']):
                counted_products[row['title']] =  (counted_products[row['title']] + (float(row['popularity']) * float(row['quantity'])))
            else:
                counted_products[row['title']] = float(row['popularity']) * float(row['quantity'])
    sorted_tuples = sorted(counted_products.items(), key=operator.itemgetter(1), reverse=True)[:products_num]
    return [{'product_title':i[0], 'popularity': i[1]} for i in sorted_tuples]

    



    
    



