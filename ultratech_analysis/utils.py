import datetime

from chemical_analysis.utils import truncate
import psycopg2
import logging
import os

LOGGER = logging.getLogger('django')


def format_filter_response(data):
    response = dict()
    response['plant'] = set()
    response['truck_type'] = set()
    response['i2_taluka_desc'] = set()
    response['city'] = set()
    for each in data:
        if str(each.get('plant_name')):
            response['plant'].add(str(each.get('plant')) + "-" + str(each.get('plant_name')))
        response['truck_type'].add(each.get('truck_type'))
        if str(each.get('i2_taluka_desc')):
            response['i2_taluka_desc'].add(each.get('i2_taluka_desc'))
        response['city'].add(str(each.get('city_code')) + "-" + str(each.get('city_desc')))
    return response


def format_dashboard_response(data, current_data, route):
    response = dict()
    response['otherData'] = list()
    response['simiPTPK'] = list()
    response['routeData'] = list()
    for each_data in data:
        other_data = dict()
        other_data['source_location'] = [each_data.source_lat, each_data.source_long]
        other_data['location'] = [each_data.latitude, each_data.longitude]
        other_data['simi_route'] = each_data.simi_city
        other_data['city'] = str(each_data.simi_city_code) + "-" + str(each_data.type)
        simi_ptpk = dict()
        simi_ptpk['nh_per'] = truncate(each_data.nh_per_ref, 2)
        simi_ptpk['sh_per'] = each_data.sh_per_ref
        simi_ptpk['hilly_per'] = each_data.hilly_per_ref
        simi_ptpk['plain_per'] = truncate(each_data.plain_per_ref, 0)
        simi_ptpk['mean_ele'] = truncate(each_data.mean_ele, 0)
        simi_ptpk['sd_ele'] = truncate(each_data.sd_ele, 0)
        simi_ptpk['simi_route'] = each_data.simi_city
        simi_ptpk['ptpk'] = truncate(each_data.ptpk, 2)
        simi_ptpk['ptpkPred'] = truncate(each_data.ptpk_pred, 2)
        simi_ptpk['latitude'] = each_data.latitude
        simi_ptpk['longitude'] = each_data.longitude
        simi_ptpk['source_lat'] = each_data.source_lat
        simi_ptpk['source_long'] = each_data.source_long
        simi_ptpk['avgQuantity'] = truncate(each_data.quantity, 0)
        simi_ptpk['avgLead'] = truncate(each_data.lead, 0)
        simi_ptpk['avgTravelTime'] = truncate(each_data.onward_travel, 2)
        simi_ptpk['avg_simi_coeff'] = truncate(each_data.simi_coeff, 2)
        simi_ptpk['total_restriction_time'] = each_data.total_restriction_time
        simi_ptpk['city'] = str(each_data.simi_city_code) + "-" + str(each_data.type) + " " + str(each_data.i2_taluka_desc)
        simi_ptpk['integration_flag'] = each_data.integration_flag
        simi_ptpk['cluster_flag'] = each_data.cluster_flag
        simi_ptpk['union_flag'] = each_data.union_flag

        response['otherData'].append(other_data)
        response['simiPTPK'].append(simi_ptpk)

    for each_data in route:
        route_data = dict()
        route_data['route_1'] = each_data.route_1
        route_data['impact'] = truncate(each_data.impact, 0)
        route_data['lead'] = truncate(each_data.lead, 0)
        route_data['quantity'] = truncate(each_data.quantity, 0)
        route_data['simiCoeff'] = truncate(each_data.simi_coeff, 2)
        route_data['PTPK'] = truncate(each_data.ptpk, 2)
        response['routeData'].append(route_data)

    if current_data:
        response['source'] = current_data.full_plant_name
        response['destination'] = current_data.simi_city_name
        response['ptpkPred'] = truncate(current_data.ptpk_pred, 2)
        response['currPtpk'] = truncate(current_data.ptpk, 2)
        response['currQuantity'] = truncate(current_data.quantity, 2)

    return response


con = None


def lit_database_connection():
    global con
    try:
        if con:
            try:
                with con.cursor() as cur:
                    cur.execute('SELECT 1')
                    LOGGER.info("old connection is live")
            except (psycopg2.OperationalError, Exception):
                con.close()
                con = psycopg2.connect(dbname=os.environ.get('LIT_DBNAME'),
                                       host=os.environ.get('LIT_HOST'),
                                       user=os.environ.get('LIT_USER'),
                                       password=os.environ.get('LIT_PASSWORD'),
                                       port=os.environ.get('LIT_PORT'))
                LOGGER.info("unable to use last connection, new lit connection is created")
        else:
            con = psycopg2.connect(dbname=os.environ.get('LIT_DBNAME'),
                                   host=os.environ.get('LIT_HOST'),
                                   user=os.environ.get('LIT_USER'),
                                   password=os.environ.get('LIT_PASSWORD'),
                                   port=os.environ.get('LIT_PORT'))
            LOGGER.info("LIT DB connection is created first time")
    except Exception as ex:
        LOGGER.exception("not able to establish lit connection")
    return con


def get_month_no_from_name(month_name):
    long_month_name = month_name
    long_month_name = long_month_name.strip()
    datetime_object = datetime.datetime.strptime(long_month_name, "%b")
    month_number = datetime_object.month
    return month_number


threaded_postgresql_pool = None


def get_lit_connection_pool():
    from psycopg2 import pool
    global threaded_postgresql_pool
    if not threaded_postgresql_pool:
        threaded_postgresql_pool = psycopg2.pool.ThreadedConnectionPool(10, 20,
                                                                        user=os.environ.get('LIT_USER'),
                                                                        password=os.environ.get('LIT_PASSWORD'),
                                                                        host=os.environ.get('LIT_HOST'),
                                                                        port=os.environ.get('LIT_PORT'),
                                                                        database=os.environ.get('LIT_DBNAME'))
    return threaded_postgresql_pool
