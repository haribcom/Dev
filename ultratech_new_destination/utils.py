import requests
import urllib.parse
import psycopg2
import os
from django.db import connections


def get_address_lat_long(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return response[0]["lat"], response[0]["lon"]


def get_data(select_fields, where_fields, where_in_fields):
    cur = connections['ultra_tech'].cursor()
    sql_text = format_sql(select_fields, where_fields, where_in_fields)
    cur.execute(sql_text)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    return colnames, result


def format_sql(select_fields, where_fields=None, where_in_fields=None):
    sql = "select {} from dna_ultratech_fare_dev.dispatchdata_newdestination_org as a INNER JOIN dna_ultratech_fare_dev.plant_metadata as b ON  b.plant_code = a.delvry_plant  {} ;"
    where = ""
    count = 0
    where_len = len(where_fields)
    if where_fields or where_in_fields:
        where = " where "
        for key in where_fields:
            count = count + 1
            if count == where_len and not where_in_fields:
                where = where + key + "='" + str(where_fields[key]) + "' "
            else:
                where = where + key + "='" + str(where_fields[key]) + "' AND "
        count = 0
        for key in where_in_fields:
            count = count + 1
            if count == len(where_in_fields):
                where = where + key + " in ('" + "','".join(where_in_fields[key]) + "') "
                # where = where + key + " in " + str(where_in_fields[key]) + " "
            else:
                where = where + key + " in ('" + "','".join(where_in_fields[key]) + "') AND "
                # where = where + key + " in " + str(where_in_fields[key]) + " AND "

    sql = sql.format(", ".join(select_fields), where)
    return sql


def format_filter_response(columnnames, result_data, fields, response=None):
    response = response if response != None else dict()
    for field_name in fields:
        response[field_name] = set()
        for each_result in result_data:
            response[field_name].add("-".join(each_result))

    return response


def check_plant_access(user, plant):
    try:
        allowed_plants = user.extra_permissions.get('utcl_plants')
        if int(plant) in allowed_plants:
            return True
    except Exception as ex:
        return False
    return False


def get_allowed_plants(user):
    try:
        return user.extra_permissions.get('utcl_plants')
    except Exception as ex:
        return []


def populate_xlxs(workbook, Mapper, model_name, plant_destination):
    row, col = 0, 0
    worksheet = workbook.add_worksheet("{}_data".format(model_name))
    worksheet.freeze_panes(1, 0)
    bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})

    for column_name in Mapper.keys():
        worksheet.write(row, col, column_name, bold)
        col += 1
    col = 0
    row += 1

    for obj in getattr(plant_destination, model_name).all():
        for key, value in Mapper.items():
            worksheet.write(row, col, getattr(obj, Mapper[key]))
            col += 1
        col = 0
        row += 1