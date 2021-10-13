import math
import logging

from django.contrib.auth import get_user_model

LOGGER = logging.getLogger(__name__)


def list_of_similarity_field(query, chemicals=False, ultra_tech=False):
    """
    This fn takes care of drop down need to be shown on the similarity dashboard
    :param ultra_tech:
    :param query:
    :param chemicals:
    :return:
    """
    response = list()
    each_response = dict()
    response.append(each_response)
    plant = set()
    taluka = set()
    path_selected = set()
    slab = set()
    truck_type = set()
    type = set()
    direct_sto = set()
    city_code = set()
    if chemicals:
        product = set()

    for each_relation in query:
        plant.add(each_relation.get('plant'))
        taluka.add(each_relation.get('taluka'))
        path_selected.add(each_relation.get('route'))
        slab.add(each_relation.get('slab'))
        truck_type.add(each_relation.get('truck_type'))
        direct_sto.add(each_relation.get('direct_sto'))
        if chemicals:
            product.add(each_relation.get('product'))
            type.add(each_relation.get('type'))
        if ultra_tech:
            type.add(each_relation.get('t_type'))
            city_code.add(each_relation.get('city_code'))

    each_response['plant'] = list(plant)
    each_response['taluka'] = list(taluka)
    each_response['pathSelected'] = list(path_selected)
    each_response['slab'] = list(slab)
    each_response['truckType'] = list(truck_type)
    each_response['type'] = list(type)
    each_response['directSTO'] = list(direct_sto)
    each_response['city_code'] = list(city_code)
    if chemicals:
        each_response['product'] = list(product)
    return response


def remove_simi_coeff_1(query, key):
    """
    This fn removes the simi coeff of data which is equal to 1
    :param query:
    :param key:
    :return:
    """
    for each_route in query:
        if each_route[key] == 1 or each_route[key] == 1.0:
            query.remove(each_route)
    return query


def route(route_query):
    """
    Fn to mark the route as optimized and unoptimized
    :param route_query:  
    :return: 
    """
    # else:
    for each_route in route_query:
        if each_route['PTPK'] and each_route['PTPK_Pred']:
            if each_route['PTPK'] <= each_route['PTPK_Pred']:
                each_route['optimized'] = 'optimized'
            else:
                each_route['optimized'] = 'Not optimized'
        else:
            each_route['optimized'] = 'Not optimized'
    return route_query


def add_location_graph(query, location="location", latitude="latitude", longitude="longitude"):
    """
    This is the query from the db containing lat and long. This fn will add
    location as a [lat,long] to display in graph
    :param longitude:
    :param latitude:
    :param location:
    :param query:
    :return:
    """
    for each_data in query:
        each_data[location] = [each_data[latitude], each_data[longitude]]
    return query


def truncate(number, digits=0) -> float:  # Todo: use from core/utils
    """
    Fn to truncate float values up to req decimal places
    :param number:
    :param digits:
    :return:
    """
    try:
        if digits == 0:
            return round(number, digits)
        number = float(number)
        before_deci, after_deci = str(number).split('.')
        return float(before_deci + "." + after_deci[0:digits])
    except:
        return number


def capitalize(data, key):
    """
    function to change capitalize only first letter of string
    :param data: list of dict
    :param key: value of which key you want to capitalize
    :return:
    """
    for info in data:
        info[key] = "-".join(value.capitalize() for value in info.get(key).split('-')) if info[key] else None


def add_spacing(data, key):
    """
    :param data: list of dict
    :param key: value of which key you want to format
    :return:
    """
    for info in data:
        info[key] = " - ".join(value for value in info.get(key).split('-')) if info[key] else None
