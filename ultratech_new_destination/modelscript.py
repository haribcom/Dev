# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 18:57:55 2020

@author: soumita.dasgupta-ne
"""

#########################################################################################
import os

from ultratech_new_destination.googlemockdata import geocode_latlong_response, distance_matrix_response, \
    elev_url_response, \
    elevation_extraction_response

'''
import libraries

'''

import pandas as pd
import numpy as np
import googlemaps  # for geocoding
from googlemaps import Client as GoogleMaps
import matplotlib.pyplot as plt
# import geopandas as gpd
from shapely.geometry import Polygon, Point
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import math
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import scipy.stats

warnings.filterwarnings("ignore")
import logging as log
import requests
import json
# import mysql.connector
# import MySQLdb
from pandas import DataFrame
import psycopg2
import statistics
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
from datetime import datetime
from django.db import connections
from shapely.geometry import Point, LineString

##########################################################################################
from django.conf import settings

'''
Data import

'''

gmap_api_count = 0
# db_name = os.environ.get('NEW_DESTINATION_DB_NAME')
# db_host = os.environ.get('NEW_DESTINATION_DB_HOST')
# db_user = os.environ.get('NEW_DESTINATION_DB_USER')
# db_password = os.environ.get('NEW_DESTINATION_DB_PASSWORD')
map_data = None
map_data_result = dict()
map_data_result['distance_matrix'] = dict()
map_data_result['elev_url'] = dict()
map_data_result['elevation_extraction'] = dict()
map_data_result['reverse_geocode'] = dict()

''' postgre connection'''

# con = psycopg2.connect(dbname=db_name,
#                        host=db_host, user=db_user,
#                        password=db_password)

# ''' Hierarchy data'''
#
# cur = con.cursor()
# cur.execute("select * from dna_ultratech_fare_dev.hierarchydata_org")
# colnames = [desc[0] for desc in cur.description]
# result = cur.fetchall()
# Hier = DataFrame(result, columns=colnames)
#
# ''' basefreight_newdestination data'''
#
# cur1 = con.cursor()
# cur1.execute("select * from dna_ultratech_fare_dev.basefreightdata_newdestination_org")
# colnames1 = [desc[0] for desc in cur1.description]
# result1 = cur1.fetchall()
# all_bf = DataFrame(result1, columns=colnames1)
#
# all_bf.rename(
#     columns={"plant_code": "PLANT_CODE", "city_code": "CITY_CODE", "special_process_indi": "SPECIAL_PROCESS_INDI",
#              "toll_rate": "TOLL_RATE", "unloading": "UNLOADING"}, inplace=True)
#
# all_bf = all_bf[["PLANT_CODE", "CITY_CODE", "SPECIAL_PROCESS_INDI", "TOLL_RATE", "UNLOADING"]]
# all_bf["PLANT_CODE"] = all_bf['PLANT_CODE'].apply(str)

''' dispatch_newdestination data'''

# cur2 = con.cursor()
dispatchdata = None

''' simi_new_destination data'''

# cur3 = con.cursor()
simi_data = None

hierarchydata = None

bf = None
kd = None


####################################################################################################


#############################################################################################
def get_data_from_db(plant,taluka):
    global dispatchdata, bf, kd, simi_data
    cur = connections['ultra_tech'].cursor()
    cur.execute(
        "select * from dna_ultratech_fare_dev.dispatchdata_newdestination_org  where delvry_plant=""'" + plant + "'"";")
    colnames2 = [desc[0] for desc in cur.description]
    result2 = cur.fetchall()
    dispatchdata = DataFrame(result2, columns=colnames2)

    dispatchdata.rename(columns={"delvry_plant": "DELVRY_PLANT", "city_code": "CITY_CODE", "truck_type": "TRUCK_TYPE",
                                 "quantity": "QUANTITY", "state_desc": "STATE_DESC", "district_desc": "DISTRICT_DESC",
                                 "i2_taluka": "I2_TALUKA", "i2_taluka_desc": "I2_TALUKA_DESC", "city_desc": "CITY_DESC",
                                 "lead": "Lead", "base_freight": "Base.freight", "ptpk": "PTPK",
                                 "direct_sto": "Direct_STO",
                                 "zone": "Zone", "source_lat": "Source_Lat", "source_long": "Source_Long", "lat": "lat",
                                 "long": "Long", "slab_new": "Slab_new", "google_dist": "Google_Dist",
                                 "toll_rate": "TOLL_RATE", "unloading": "UNLOADING"}, inplace=True)

    dispatchdata["DELVRY_PLANT"] = dispatchdata["DELVRY_PLANT"].apply(str)
    dispatchdata.drop(['Zone'], axis=1, inplace=True)

    # dispatchdata = dispatchdata.merge(all_bf, how='left', left_on=["DELVRY_PLANT", "CITY_CODE", "TRUCK_TYPE"],
    # right_on=["PLANT_CODE", "CITY_CODE", "SPECIAL_PROCESS_INDI"])
    dispatchdata['TOLL_RATE'].fillna(0, inplace=True)
    dispatchdata['UNLOADING'].fillna(0, inplace=True)

    mask = dispatchdata['CITY_CODE'].isin(["IE33", "IE28"])
    dispatchdata = dispatchdata[~mask]

    dispatchdata["Taluka_input"] = dispatchdata['I2_TALUKA'] + "-" + dispatchdata['I2_TALUKA_DESC']

    bf = dispatchdata.copy()
    kd = dispatchdata[dispatchdata['QUANTITY'] != 0]  # there is some dispatch in between plant to dest

    cur.execute("select * from dna_ultratech_fare_dev.simiinput_newdestination_org")
    colnames3 = [desc[0] for desc in cur.description]
    result3 = cur.fetchall()
    simi_data = DataFrame(result3, columns=colnames3)

    simi_data.rename(columns={"plant": "PLANT", "city_code": "CITY_CODE", "type": "Type", "truck_type": "TRUCK_TYPE",
                              "direct_sto": "Direct_STO", "plain": "Plain", "hilly": "Hilly", "nh_dist": "NH_Dist",
                              "sh_dist": "SH_Dist", "other_dist": "Other_Dist",
                              "total_dist_google": "Total_Dist_Google",
                              "nh_per": "NH_Per", "sh_per": "SH_Per", "other_dist": "Other_Dist",
                              "total_dist_google": "Total_Dist_Google", "nh_per": "NH_Per", "sh_per": "SH_Per",
                              "other_per": "Other_Per", "lead": "Lead", "ptpk": "PTPK", "plain_per": "Plain_Per",
                              "hilly_per": "Hilly_Per", "otd": "OTD", "rtd": "RTD", "itc": "ITC", "slab": "Slab",
                              "quantity": "QUANTITY", "i2_taluka_desc": "I2_TALUKA_DESC"},
                     inplace=True)
    ''' hierarchy data'''

    cur.execute(
        "select * from dna_ultratech_fare_dev.hierarchydata_org  where i2_taluka=""'" + taluka.split("-")[0] + "'"";")
    colnames2 = [desc[0] for desc in cur.description]
    result2 = cur.fetchall()
    hierarchydata = DataFrame(result2, columns=colnames2)

    # bf = dispatchdata.copy()
    # kd = dispatchdata[dispatchdata['QUANTITY'] != 0]  # there is some dispatch in between plant to dest

    # dispatchdata['Taluka_input'] = dispatchdata['I2_TALUKA'] + "-" + dispatchdata['I2_TALUKA_DESC']


#############################################################################################
'''
validate coordinate code (check)

'''


def Validate_coordinate(LAT, LONG):  # if the lat long lies IN India or not #check 4 extreme points
    if 6.0 <= LAT <= 40.0 and 69.0 <= LONG <= 96.0:
        return True
    else:
        return False


##############################################################################################


#####################################################################################################

'''
Geocoding

'''

key = os.environ.get('GOOGLE_MAP_KEY')


def Geocode_latlong(address, key):
    gmaps = googlemaps.Client(key)
    geocode_result = gmaps.geocode(address)  # if not settings.MOCK else geocode_latlong_response

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    location_type = geocode_result[0]["geometry"]["location_type"]
    formatted_address = geocode_result[0]["formatted_address"]
    # test - print results
    return (lat, lon, location_type, formatted_address)


'''
Reverse geocoding: getting address from lat long
'''


def reverse_geocode(latlng, key):
    global gmap_api_count
    gmaps = googlemaps.Client(key)
    if map_data:
        try:
            reverse_geocode_result = map_data['reverse_geocode'][str((latlng))]
        except KeyError as kex:
            reverse_geocode_result = gmaps.reverse_geocode(latlng)
            gmap_api_count = gmap_api_count + 1
    else:
        reverse_geocode_result = gmaps.reverse_geocode(latlng)
        gmap_api_count = gmap_api_count + 1
        map_data_result['reverse_geocode'][str((latlng))] = reverse_geocode_result
    formatted_address = reverse_geocode_result[0]['formatted_address']
    # test - print results
    return formatted_address


####################################################################################################


'''
function to get plant lat long 

'''


def Plant_Lat_Long(PLANT, bf):
    bf1 = bf[bf["DELVRY_PLANT"] == PLANT]
    bf1.reset_index(drop=True, inplace=True)
    Source_Lat = bf1[bf1["DELVRY_PLANT"] == PLANT]["Source_Lat"][0]
    Source_Long = bf1[bf1["DELVRY_PLANT"] == PLANT]["Source_Long"][0]
    data = [[PLANT, Source_Lat, Source_Long]]
    PLANT_LAT_LONG = pd.DataFrame(data, columns=["PLANT", "Source_Lat", "Source_Long"])
    return PLANT_LAT_LONG


#################################################################################################

'''
find out distance from source to destination

'''


def distance_matrix(lat1, long1, lat2, long2, key):
    global gmap_api_count
    gmaps = googlemaps.Client(key)
    if map_data:
        try:
            try:
                distance_result = map_data['distance_matrix'][str((lat1[0], long1[0], lat2, long2))]
            except:
                distance_result = map_data['distance_matrix'][str((lat1[0], long1[0], lat2[0], long2[0]))]
        except (KeyError, IndexError, TypeError) as kex:
            distance_result = gmaps.distance_matrix((lat1, long1), (lat2, long2))
            gmap_api_count = gmap_api_count + 1
    else:
        distance_result = gmaps.distance_matrix((lat1, long1),
                                                (lat2, long2))  # if not settings.MOCK else distance_matrix_response
        gmap_api_count = gmap_api_count + 1
        try:
            map_data_result['distance_matrix'][str((lat1[0], long1[0], lat2, long2))] = distance_result
        except:
            map_data_result['distance_matrix'][str((lat1[0], long1[0], lat2[0], long2[0]))] = distance_result
    distance = round(distance_result['rows'][0]['elements'][0]['distance']['value'] / 1000, 0)
    # test - print results
    return distance


def distance_matrix1(lat1, long1, lat2, long2, key, waypoints):
    gmaps = googlemaps.Client(key)
    if waypoints.size != 0:
        wpt = []
        for i in range(len(waypoints)):
            wpt.append("via:" + str(waypoints[i][0]) + "," + str(waypoints[i][1]))

        # Get the Direction
        check1 = gmaps.directions(origin=(lat1, long1), destination=(lat2, long2), waypoints=wpt)
    else:
        check1 = gmaps.directions(origin=(lat1, long1), destination=(lat2, long2))
    distance = round(check1[0]['legs'][0]['distance']['value'] / 1000, 0)

    return distance


#####################################################################################################

'''
lead proposed

'''


def lead_proposed(PLANT, taluka, LAT, LONG, DIRECT_STO, dispatchdata, dist, out):
    new_destination_google_lead = dist
    new_destination_lat = LAT

    new_destination_long = LONG
    d1 = np.nan
    d2 = np.nan

    lead_up = new_destination_google_lead + new_destination_google_lead * 0.15
    lead_lower = new_destination_google_lead - new_destination_google_lead * 0.15

    df = dispatchdata[(dispatchdata['DELVRY_PLANT'] == PLANT) & (dispatchdata['Direct_STO'] == DIRECT_STO.upper()) & (
            dispatchdata['Lead'] <= lead_up) & (dispatchdata['Lead'] >= lead_lower)]

    df.reset_index(drop=True, inplace=True)
    if len(df) != 0:
        df['lat'] = df['lat'].astype(float)
        df['Long'] = df['Long'].astype(float)
        source = Point(float(df['Source_Lat'][0]), float(df['Source_Long'][0]))  # Plant Lat-Long
        new_dest = Point(LAT, LONG)  # New destination Lat-Long
        dist1 = source.distance(new_dest)  # Distance between Source and New-Destination

        plant_newdest_cir = source.buffer(
            dist1)  # Circle taking Source as center and Radius as distance (Source-New_Destination)
        newdest_cir = new_dest.buffer(dist1)  # Cirlce considering New-Destination as center
        Area_greater = newdest_cir.difference(plant_newdest_cir)  # for distance more than New-Destination
        Area_smaller = newdest_cir.intersection(plant_newdest_cir)  # for distance less than New-Destination

        # Points in Area_smaller
        points_smaller = MultiPoint([Point(df['lat'][i], df['Long'][i]) for i in range(len(df)) if
                                     Point(df['lat'][i], df['Long'][i]).within(Area_smaller)])
        points_greater = MultiPoint([Point(df['lat'][i], df['Long'][i]) for i in range(len(df)) if
                                     Point(df['lat'][i], df['Long'][i]).within(Area_greater)])

        try:
            # Smallest Point
            point_smallest = nearest_points(new_dest, points_smaller)[1]
            df_smaller = df[df['lat'] == point_smallest.x]
            df_smaller.reset_index(drop=True, inplace=True)
            df_smaller1 = [[df_smaller['CITY_DESC'][0], df_smaller['I2_TALUKA_DESC'][0], df_smaller['Lead'][0],
                            df_smaller['Google_Dist'][0], df_smaller['PTPK'][0], df_smaller['Base.freight'][0],
                            df_smaller['QUANTITY'][0], df_smaller['TOLL_RATE'][0], df_smaller['UNLOADING'][0],
                            df_smaller['lat'][0], df_smaller['Long'][0]]]

            Nearest_smaller_point = pd.DataFrame(df_smaller1,
                                                 columns=["NEAREST_SMALLER_CITY_NAME", "NEAREST_SMALLER_TALUKA_NAME",
                                                          "NEAREST_SMALLER_LEAD", "NEAREST_SMALLER_Google_Dist",
                                                          "NEAREST_SMALLER_PTPK", "NEAREST_SMALLER_BASE_FREIGHT",
                                                          "NEAREST_SMALLER_QUANTITY", "NEAREST_SMALLER_TOLL",
                                                          "NEAREST_SMALLER_UNLOADING", "NEAREST_SMALLER_lat",
                                                          "NEAREST_SMALLER_long"])

        except:
            df_smaller1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

            Nearest_smaller_point = pd.DataFrame(df_smaller1,
                                                 columns=["NEAREST_SMALLER_CITY_NAME", "NEAREST_SMALLER_TALUKA_NAME",
                                                          "NEAREST_SMALLER_LEAD", "NEAREST_SMALLER_Google_Dist",
                                                          "NEAREST_SMALLER_PTPK", "NEAREST_SMALLER_BASE_FREIGHT",
                                                          "NEAREST_SMALLER_QUANTITY", "NEAREST_SMALLER_TOLL",
                                                          "NEAREST_SMALLER_UNLOADING", "NEAREST_SMALLER_lat",
                                                          "NEAREST_SMALLER_long"])

        try:
            point_greatest = nearest_points(new_dest, points_greater)[1]
            df_greater = df[df["lat"] == point_greatest.x]
            df_greater.reset_index(drop=True, inplace=True)
            df_greater1 = [[df_greater['CITY_DESC'][0], df_greater['I2_TALUKA_DESC'][0], df_greater['Lead'][0],
                            df_greater['Google_Dist'][0], df_greater['PTPK'][0], df_greater['Base.freight'][0],
                            df_greater['QUANTITY'][0], df_greater['TOLL_RATE'][0], df_greater['UNLOADING'][0],
                            df_greater['lat'][0], df_greater['Long'][0]]]

            Nearest_greater_point = pd.DataFrame(df_greater1,
                                                 columns=["NEAREST_GREATER_CITY_NAME", "NEAREST_GREATER_TALUKA_NAME",
                                                          "NEAREST_GREATER_LEAD", "NEAREST_GREATER_Google_Dist",
                                                          "NEAREST_GREATER_PTPK", "NEAREST_GREATER_BASE_FREIGHT",
                                                          "NEAREST_GREATER_QUANTITY", "NEAREST_GREATER_TOLL",
                                                          "NEAREST_GREATER_UNLOADING", "NEAREST_GREATER_lat",
                                                          "NEAREST_GREATER_long"])
        except:
            df_greater1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

            Nearest_greater_point = pd.DataFrame(df_greater1,
                                                 columns=["NEAREST_GREATER_CITY_NAME", "NEAREST_GREATER_TALUKA_NAME",
                                                          "NEAREST_GREATER_LEAD", "NEAREST_GREATER_Google_Dist",
                                                          "NEAREST_GREATER_PTPK", "NEAREST_GREATER_BASE_FREIGHT",
                                                          "NEAREST_GREATER_QUANTITY", "NEAREST_GREATER_TOLL",
                                                          "NEAREST_GREATER_UNLOADING", "NEAREST_GREATER_lat",
                                                          "NEAREST_GREATER_long"])

        nearest_point_lead = pd.concat([Nearest_greater_point, Nearest_smaller_point], axis=1)
        nearest_point_lead.reset_index(drop=True, inplace=True)
    else:
        df_smaller1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

        Nearest_smaller_point = pd.DataFrame(df_smaller1,
                                             columns=["NEAREST_SMALLER_CITY_NAME", "NEAREST_SMALLER_TALUKA_NAME",
                                                      "NEAREST_SMALLER_LEAD", "NEAREST_SMALLER_Google_Dist",
                                                      "NEAREST_SMALLER_PTPK", "NEAREST_SMALLER_BASE_FREIGHT",
                                                      "NEAREST_SMALLER_QUANTITY", "NEAREST_SMALLER_TOLL",
                                                      "NEAREST_SMALLER_UNLOADING", "NEAREST_SMALLER_lat",
                                                      "NEAREST_SMALLER_long"])

        df_greater1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

        Nearest_greater_point = pd.DataFrame(df_greater1,
                                             columns=["NEAREST_GREATER_CITY_NAME", "NEAREST_GREATER_TALUKA_NAME",
                                                      "NEAREST_GREATER_LEAD", "NEAREST_GREATER_Google_Dist",
                                                      "NEAREST_GREATER_PTPK", "NEAREST_GREATER_BASE_FREIGHT",
                                                      "NEAREST_GREATER_QUANTITY", "NEAREST_GREATER_TOLL",
                                                      "NEAREST_GREATER_UNLOADING", "NEAREST_GREATER_lat",
                                                      "NEAREST_GREATER_long"])

        nearest_point_lead = pd.concat([Nearest_greater_point, Nearest_smaller_point], axis=1)
        nearest_point_lead.reset_index(drop=True, inplace=True)

    if np.isnan(nearest_point_lead['NEAREST_SMALLER_Google_Dist'][0]) == False:
        d1 = float(nearest_point_lead['NEAREST_SMALLER_LEAD'][0]) - nearest_point_lead['NEAREST_SMALLER_Google_Dist'][0]

    if np.isnan(nearest_point_lead['NEAREST_GREATER_Google_Dist'][0]) == False:
        d2 = float(nearest_point_lead['NEAREST_GREATER_LEAD'][0]) - nearest_point_lead['NEAREST_GREATER_Google_Dist'][0]

    if np.isnan(d1) == False and np.isnan(d2) == False:
        d = [d1, d2]
        out['Proposed_Lead'] = out['DISTANCE_SOURCE_NEWDESTINATION'] + statistics.mean(d)
        out["Comment_lead"] = "Nearest smaller city name (Lead/ Google dist): " + \
                              nearest_point_lead["NEAREST_SMALLER_CITY_NAME"][0] + "(" + str(
            np.int(nearest_point_lead["NEAREST_SMALLER_LEAD"][0])) + "/" + \
                              nearest_point_lead["NEAREST_SMALLER_Google_Dist"][0].astype(
                                  str) + ")" + "," + "Nearest greater city name(Lead/ Google dist): " + \
                              nearest_point_lead["NEAREST_GREATER_CITY_NAME"][0] + "(" + str(
            np.int(nearest_point_lead["NEAREST_GREATER_LEAD"][0])) + "/" + \
                              nearest_point_lead["NEAREST_GREATER_Google_Dist"][0].astype(
                                  str) + ")" + "," + "avg of the diff between lead and google distance: " + str(
            statistics.mean(d)) + "," + "New Destination google lead: " + out['DISTANCE_SOURCE_NEWDESTINATION'][
                                  0].astype(str)

    elif np.isnan(d1) == True and np.isnan(d2) == False:
        d = [d2]
        out['Proposed_Lead'] = out['DISTANCE_SOURCE_NEWDESTINATION'] + d2
        out["Comment_lead"] = "Nearest smaller city name (Lead/ Google dist): " + str(
            nearest_point_lead["NEAREST_SMALLER_CITY_NAME"][0]) + "(" + nearest_point_lead["NEAREST_SMALLER_LEAD"][
                                  0].astype(str) + "/" + nearest_point_lead["NEAREST_SMALLER_Google_Dist"][0].astype(
            str) + ")" + "," + "Nearest greater city name(Lead/Google dist): " + \
                              nearest_point_lead["NEAREST_GREATER_CITY_NAME"][0] + "(" + str(
            np.int(nearest_point_lead["NEAREST_GREATER_LEAD"][0])) + "/" + \
                              nearest_point_lead["NEAREST_GREATER_Google_Dist"][0].astype(
                                  str) + ")" + "," + "avg of the diff between lead and google distance: " + str(
            d) + "," + "New Destination google lead: " + out['DISTANCE_SOURCE_NEWDESTINATION'][0].astype(str)


    elif np.isnan(d1) == False and np.isnan(d2) == True:
        d = [d1]
        out['Proposed_Lead'] = out['DISTANCE_SOURCE_NEWDESTINATION'] + d1
        out["Comment_lead"] = "Nearest smaller city name (Lead/ Google dist): " + \
                              nearest_point_lead["NEAREST_SMALLER_CITY_NAME"][0] + "(" + str(
            np.int(nearest_point_lead["NEAREST_SMALLER_LEAD"][0])) + "/" + \
                              nearest_point_lead["NEAREST_SMALLER_Google_Dist"][0].astype(
                                  str) + ")" + "," + "Nearest greater city name(Lead/ Google dist): " + str(
            nearest_point_lead["NEAREST_GREATER_CITY_NAME"][0]) + "(" + nearest_point_lead["NEAREST_GREATER_LEAD"][
                                  0].astype(str) + "/" + nearest_point_lead["NEAREST_GREATER_Google_Dist"][0].astype(
            str) + ")" + "," + "avg of the diff between lead and google distance: " + str(
            d) + "," + "New Destination google lead: " + out['DISTANCE_SOURCE_NEWDESTINATION'][0].astype(str)

    elif np.isnan(d1) == True and np.isnan(d2) == True:
        out['Proposed_Lead'] = out['DISTANCE_SOURCE_NEWDESTINATION'] + 0
        out["Comment_lead"] = "Nearest smaller city name (Lead/ Google dist): " + str(
            nearest_point_lead["NEAREST_SMALLER_CITY_NAME"][0]) + "(" + nearest_point_lead["NEAREST_SMALLER_LEAD"][
                                  0].astype(str) + "/" + nearest_point_lead["NEAREST_SMALLER_Google_Dist"][0].astype(
            str) + ")" + "," + "Nearest greater city name(Lead/ Google dist): " + str(
            nearest_point_lead["NEAREST_GREATER_CITY_NAME"][0]) + "(" + nearest_point_lead["NEAREST_GREATER_LEAD"][
                                  0].astype(str) + "/" + nearest_point_lead["NEAREST_GREATER_Google_Dist"][0].astype(
            str) + ")" + "," + "avg of the diff between lead and google distance: " + str(
            0) + "," + "New Destination google lead: " + out['DISTANCE_SOURCE_NEWDESTINATION'][0].astype(str)

    return out

'''
slab creation

'''


def slab_new(df):
    df['Slab_new'] = pd.cut(df['Proposed_Lead'],
                            bins=[0, 25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400, 1000],
                            labels=['0-25', '26-50', '51-75', '76-100', '101-125', '126-150', '151-175', '176-200',
                                    '201-250', '251-300', '301-350', '351-400', ">400"])
    return df


def slab_new1(df):
    df['Slab_new'] = pd.cut(df['Lead'], bins=[0, 25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400, 1000],
                            labels=['0-25', '26-50', '51-75', '76-100', '101-125', '126-150', '151-175', '176-200',
                                    '201-250', '251-300', '301-350', '351-400', ">400"])
    return df


def PTPK_pred_TalukaAnalysis1(taluka, PLANT, TRUCK_TYPE, DIRECT_STO, out, dispatchdata, nearest_point, Pred_PTPK,
                              nearest_comment, hierarchydata, address1):
    new_destination_lead = out["Proposed_Lead"][0]
    out1 = slab_new(out)

    new_destination_google_lead = out1["DISTANCE_SOURCE_NEWDESTINATION"][0]  # This will come from Google API

    df = dispatchdata[(dispatchdata['Taluka_input'] == taluka) & (dispatchdata['DELVRY_PLANT'] == PLANT) & (
            dispatchdata['TRUCK_TYPE'] == str(TRUCK_TYPE)) & (dispatchdata['Direct_STO'] == DIRECT_STO.upper())]

    df.sort_values(by='QUANTITY', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["Lead"] = df["Lead"].astype(float)
    if pd.isna(Pred_PTPK) == True:
        if (df.empty == False) & (len(df) != 1):

            max_qty_1_lead = float(df['Lead'][0])
            max_qty_2_lead = float(df['Lead'][1])

            max_qty_1_ptpk = df['PTPK'][0]
            max_qty_2_ptpk = df['PTPK'][1]

            max_qty_1_source_lat = df['Source_Lat'][0]
            max_qty_1_source_long = df['Source_Long'][0]
            max_qty_1_dest_lat = df['lat'][0]
            max_qty_1_dest_long = df['Long'][0]

            # get google distance of first city with source
            google_lead = df['Google_Dist'][0]

            # Correction for Google Lead
            # new_destination_lead = new_destination_google_lead + (max_qty_1_lead-google_lead)
            # new_destination_lead=71
            # for coverage
            lower_limit_lead = min(max_qty_1_lead, max_qty_2_lead) - abs(max_qty_1_lead - max_qty_2_lead) * 0.2
            upper_limit_lead = max(max_qty_1_lead, max_qty_2_lead) + abs(max_qty_1_lead - max_qty_2_lead) * 0.2

            if lower_limit_lead <= new_destination_lead <= upper_limit_lead:

                slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)
                First_city_code = df['CITY_CODE'][0]
                Second_city_code = df['CITY_CODE'][1]

                First_city_name = df["CITY_DESC"][0]
                Second_city_name = df["CITY_DESC"][1]

                First_Quantity = df['QUANTITY'][0]
                Second_Quantity = df['QUANTITY'][1]

                First_Toll_rate = df['TOLL_RATE'][0]
                Second_Toll_rate = df['TOLL_RATE'][1]

                First_Unloading = df['UNLOADING'][0]
                Second_Unloading = df['UNLOADING'][1]

                First_city_lat = df['lat'][0]
                First_city_long = df['Long'][0]

                Second_city_lat = df['lat'][1]
                Second_city_long = df['Long'][1]

                Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)
                Pred_PTPK = np.round(Pred_PTPK, 2)

                Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                COMMENT = "PTPK FOUND USING REF POINTS"






            else:

                median_lead = np.median(df['Lead'])

                df_more = df[df['Lead'] >= median_lead]
                df_less = df[df['Lead'] < median_lead]

                df_more.reset_index(drop=True, inplace=True)
                df_less.reset_index(drop=True, inplace=True)
                max_lead_df_more = max(df_more["Lead"])
                min_lead_df_more = min(df_more['Lead'])
                max_lead_df_less = max(df_less['Lead'])
                min_lead_df_less = min(df_less['Lead'])

                # print("ma_more:", max_lead_df_more)
                # print("min_more:", min_lead_df_more)
                # print("max_less:", max_lead_df_less)
                # print("min_less:", min_lead_df_less)
                # print("new_destination_lead:", new_destination_lead)
                if (len(df_more) >= 2) & (len(df_less) >= 2):
                    #
                    if min_lead_df_more <= new_destination_lead <= max_lead_df_more:

                        df_more.sort_values(by='QUANTITY', ascending=False, inplace=True)
                        df_more.reset_index(drop=True, inplace=True)
                        max_qty_1_lead = df_more['Lead'][0]
                        max_qty_2_lead = df_more['Lead'][1]

                        max_qty_1_ptpk = df_more['PTPK'][0]
                        max_qty_2_ptpk = df_more['PTPK'][1]

                        First_city_code = df_more['CITY_CODE'][0]
                        Second_city_code = df_more['CITY_CODE'][1]

                        First_city_name = df_more["CITY_DESC"][0]
                        Second_city_name = df_more["CITY_DESC"][1]

                        First_Quantity = df_more['QUANTITY'][0]
                        Second_Quantity = df_more['QUANTITY'][1]

                        First_Toll_rate = df_more['TOLL_RATE'][0]
                        Second_Toll_rate = df_more['TOLL_RATE'][1]

                        First_Unloading = df_more['UNLOADING'][0]
                        Second_Unloading = df_more['UNLOADING'][1]

                        First_city_lat = df_more['lat'][0]
                        First_city_long = df_more['Long'][0]

                        Second_city_lat = df_more['lat'][1]
                        Second_city_long = df_more['Long'][1]

                        slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                        Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                        Pred_PTPK = np.round(Pred_PTPK, 2)
                        Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                        COMMENT = "PTPK FOUND USING REF POINTS"





                    elif min_lead_df_less <= new_destination_lead <= max_lead_df_less:

                        df_less.sort_values(by='QUANTITY', ascending=False, inplace=True)
                        df_less.reset_index(drop=True, inplace=True)
                        max_qty_1_lead = df_less['Lead'][0]
                        max_qty_2_lead = df_less['Lead'][1]

                        max_qty_1_ptpk = df_less['PTPK'][0]
                        max_qty_2_ptpk = df_less['PTPK'][1]

                        First_city_code = df_less['CITY_CODE'][0]
                        Second_city_code = df_less['CITY_CODE'][1]

                        First_city_name = df_less["CITY_DESC"][0]
                        Second_city_name = df_less["CITY_DESC"][1]

                        First_Quantity = df_less['QUANTITY'][0]
                        Second_Quantity = df_less['QUANTITY'][1]

                        First_Toll_rate = df_less['TOLL_RATE'][0]
                        Second_Toll_rate = df_less['TOLL_RATE'][1]

                        First_Unloading = df_less['UNLOADING'][0]
                        Second_Unloading = df_less['UNLOADING'][1]

                        First_city_lat = df_less['lat'][0]
                        First_city_long = df_less['Long'][0]

                        Second_city_lat = df_less['lat'][1]
                        Second_city_long = df_less['Long'][1]

                        slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                        Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                        Pred_PTPK = np.round(Pred_PTPK, 2)
                        Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                        COMMENT = "PTPK FOUND USING REF POINTS"




                    else:
                        diff_max_more = abs(new_destination_lead - max_lead_df_more)
                        diff_min_more = abs(new_destination_lead - min_lead_df_more)
                        diff_max_less = abs(new_destination_lead - max_lead_df_less)
                        diff_min_less = abs(new_destination_lead - min_lead_df_less)

                        if min(diff_max_more, diff_min_more, diff_max_less, diff_min_less) == diff_max_more:
                            df_more.sort_values(by='QUANTITY', ascending=False, inplace=True)
                            df_more.reset_index(drop=True, inplace=True)
                            max_qty_1_lead = df_more['Lead'][0]
                            max_qty_2_lead = df_more['Lead'][1]

                            max_qty_1_ptpk = df_more['PTPK'][0]
                            max_qty_2_ptpk = df_more['PTPK'][1]

                            First_city_code = df_more['CITY_CODE'][0]
                            Second_city_code = df_more['CITY_CODE'][1]

                            First_city_name = df_more["CITY_DESC"][0]
                            Second_city_name = df_more["CITY_DESC"][1]

                            First_Quantity = df_more['QUANTITY'][0]
                            Second_Quantity = df_more['QUANTITY'][1]

                            First_Toll_rate = df_more['TOLL_RATE'][0]
                            Second_Toll_rate = df_more['TOLL_RATE'][1]

                            First_Unloading = df_more['UNLOADING'][0]
                            Second_Unloading = df_more['UNLOADING'][1]

                            First_city_lat = df_more['lat'][0]
                            First_city_long = df_more['Long'][0]

                            Second_city_lat = df_more['lat'][1]
                            Second_city_long = df_more['Long'][1]

                            slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                            Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                            Pred_PTPK = np.round(Pred_PTPK, 2)
                            Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                            COMMENT = "PTPK FOUND USING REF POINTS"

                        elif min(diff_max_more, diff_min_more, diff_max_less, diff_min_less) == diff_min_more:
                            df_more.sort_values(by='QUANTITY', ascending=False, inplace=True)
                            df_more.reset_index(drop=True, inplace=True)
                            max_qty_1_lead = df_more['Lead'][0]
                            max_qty_2_lead = df_more['Lead'][1]

                            max_qty_1_ptpk = df_more['PTPK'][0]
                            max_qty_2_ptpk = df_more['PTPK'][1]

                            First_city_code = df_more['CITY_CODE'][0]
                            Second_city_code = df_more['CITY_CODE'][1]

                            First_city_name = df_more["CITY_DESC"][0]
                            Second_city_name = df_more["CITY_DESC"][1]

                            First_Quantity = df_more['QUANTITY'][0]
                            Second_Quantity = df_more['QUANTITY'][1]

                            First_Toll_rate = df_more['TOLL_RATE'][0]
                            Second_Toll_rate = df_more['TOLL_RATE'][1]

                            First_Unloading = df_more['UNLOADING'][0]
                            Second_Unloading = df_more['UNLOADING'][1]

                            First_city_lat = df_more['lat'][0]
                            First_city_long = df_more['Long'][0]

                            Second_city_lat = df_more['lat'][1]
                            Second_city_long = df_more['Long'][1]

                            slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                            Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                            Pred_PTPK = np.round(Pred_PTPK, 2)
                            Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                            COMMENT = "PTPK FOUND USING REF POINTS"

                        else:
                            df_less.sort_values(by='QUANTITY', ascending=False, inplace=True)
                            df_less.reset_index(drop=True, inplace=True)
                            max_qty_1_lead = df_less['Lead'][0]
                            max_qty_2_lead = df_less['Lead'][1]

                            max_qty_1_ptpk = df_less['PTPK'][0]
                            max_qty_2_ptpk = df_less['PTPK'][1]

                            First_city_code = df_less['CITY_CODE'][0]
                            Second_city_code = df_less['CITY_CODE'][1]

                            First_city_name = df_less["CITY_DESC"][0]
                            Second_city_name = df_less["CITY_DESC"][1]

                            First_Quantity = df_less['QUANTITY'][0]
                            Second_Quantity = df_less['QUANTITY'][1]

                            First_Toll_rate = df_less['TOLL_RATE'][0]
                            Second_Toll_rate = df_less['TOLL_RATE'][1]

                            First_Unloading = df_less['UNLOADING'][0]
                            Second_Unloading = df_less['UNLOADING'][1]

                            First_city_lat = df_less['lat'][0]
                            First_city_long = df_less['Long'][0]

                            Second_city_lat = df_less['lat'][1]
                            Second_city_long = df_less['Long'][1]

                            slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                            Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                            Pred_PTPK = np.round(Pred_PTPK, 2)
                            Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                            COMMENT = "PTPK FOUND USING REF POINTS"



                #                  data=[[predict_taluka[5],predict_taluka[1],predict_taluka[13],predict_taluka[7],predict_taluka[9],predict_taluka[11]],[predict_taluka[6],predict_taluka[2],predict_taluka[14],predict_taluka[8],predict_taluka[10],predict_taluka[12]]]
                #                  Reference_dataframe=pd.DataFrame(data,columns=['CITY_NAME','PTPK','LEAD','QUANTITY','TOLL','UNLOADING'])
                #
                else:
                    ref_dataframe = scenario4(Pred_PTPK, dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, PLANT,hierarchydata)
                    First_city_code = ref_dataframe[0]
                    Second_city_code = ref_dataframe[1]
                    First_city_name = ref_dataframe[2]
                    Second_city_name = ref_dataframe[3]
                    max_qty_1_ptpk = ref_dataframe[4]
                    max_qty_2_ptpk = ref_dataframe[5]
                    First_Quantity = ref_dataframe[6]
                    Second_Quantity = ref_dataframe[7]
                    First_Toll_rate = ref_dataframe[8]
                    Second_Toll_rate = ref_dataframe[9]
                    First_Unloading = ref_dataframe[10]
                    Second_Unloading = ref_dataframe[11]
                    max_qty_1_lead = ref_dataframe[12]
                    max_qty_2_lead = ref_dataframe[13]
                    First_city_lat = ref_dataframe[14]
                    Second_city_lat = ref_dataframe[15]
                    First_city_long = ref_dataframe[16]
                    Second_city_long = ref_dataframe[17]
                    new_destination_lead = ref_dataframe[18]
                    Pred_PTPK = ref_dataframe[19]
                    Pred_Base_Freight = ref_dataframe[20]
                    COMMENT = ref_dataframe[21]


        else:

            ref_dataframe = ptpk_logic3(dispatchdata, PLANT, address1, DIRECT_STO, taluka, out, TRUCK_TYPE, Pred_PTPK,
                                        new_destination_lead)
            First_city_code = ref_dataframe[0]
            Second_city_code = ref_dataframe[1]
            First_city_name = ref_dataframe[2]
            Second_city_name = ref_dataframe[3]
            max_qty_1_ptpk = ref_dataframe[4]
            max_qty_2_ptpk = ref_dataframe[5]
            First_Quantity = ref_dataframe[6]
            Second_Quantity = ref_dataframe[7]
            First_Toll_rate = ref_dataframe[8]
            Second_Toll_rate = ref_dataframe[9]
            First_Unloading = ref_dataframe[10]
            Second_Unloading = ref_dataframe[11]
            max_qty_1_lead = ref_dataframe[12]
            max_qty_2_lead = ref_dataframe[13]
            First_city_lat = ref_dataframe[14]
            Second_city_lat = ref_dataframe[15]
            First_city_long = ref_dataframe[16]
            Second_city_long = ref_dataframe[17]
            new_destination_lead = ref_dataframe[18]
            Pred_PTPK = ref_dataframe[19]
            Pred_Base_Freight = ref_dataframe[20]
            COMMENT = ref_dataframe[21]
        # print("calculating measures")
        PTPK_CHANGEperKM = (max_qty_1_ptpk - max_qty_2_ptpk) / (max_qty_1_lead - max_qty_2_lead)
        Lead_diff = (new_destination_lead - max_qty_1_lead)
        PTPK_diff_from_Ref_city1 = (Pred_PTPK - max_qty_1_ptpk)

        ref_dataframe1 = [
            [First_city_code, Second_city_code, First_city_name, Second_city_name, max_qty_1_ptpk, max_qty_2_ptpk,
             First_Quantity, Second_Quantity, First_Toll_rate, Second_Toll_rate, First_Unloading, Second_Unloading,
             max_qty_1_lead, max_qty_2_lead, First_city_lat, Second_city_lat, First_city_long, Second_city_long,
             new_destination_lead, Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM, Lead_diff, PTPK_diff_from_Ref_city1,
             COMMENT]]
        ref_dataframe11 = pd.DataFrame(ref_dataframe1,
                                       columns=["REF_CITY_CODE1", "REF_CITY_CODE2", "REF_CITY_NAME1", "REF_CITY_NAME2",
                                                "REF_CITY1_PTPK", "REF_CITY2_PTPK", "REF_QUANTITY1", "REF_QUANTITY2",
                                                "REF_TOLLRATE1", "REF_TOLLRATE2", "REF_UNLOADING1", "REF_UNLOADING2",
                                                "REF_LEAD1", "REF_LEAD2", "REF_LATITUDE1", "REF_LATITUDE2", "REF_LONG1",
                                                "REF_LONG2", "PROPOSED_LEAD", "PRED_PTPK", "PRED_BASE_FREIGHT",
                                                "PTPK_CHANGEperKM", "Lead_diff", "PTPK_diff_from_Ref_city1", "COMMENT"])

        ref_dataframe11.reset_index(drop=True, inplace=True)



    else:
        First_city_code = np.nan
        Second_city_code = np.nan
        First_city_name = np.nan
        Second_city_name = np.nan
        max_qty_1_ptpk = np.nan
        max_qty_2_ptpk = np.nan
        First_Quantity = np.nan
        Second_Quantity = np.nan
        First_Toll_rate = np.nan
        Second_Toll_rate = np.nan
        First_Unloading = np.nan
        Second_Unloading = np.nan
        max_qty_1_lead = np.nan
        max_qty_2_lead = np.nan
        First_city_lat = np.nan
        Second_city_lat = np.nan
        First_city_long = np.nan
        Second_city_long = np.nan
        new_destination_lead = out["Proposed_Lead"][0]
        Pred_PTPK = Pred_PTPK
        Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
        COMMENT = "PTPK USING NEAREST POINT" + " " + nearest_comment
        PTPK_CHANGEperKM = (max_qty_1_ptpk - max_qty_2_ptpk) / (max_qty_1_lead - max_qty_2_lead)
        Lead_diff = (new_destination_lead - max_qty_1_lead)
        PTPK_diff_from_Ref_city1 = (Pred_PTPK - max_qty_1_ptpk)

        ref_dataframe1 = [
            [First_city_code, Second_city_code, First_city_name, Second_city_name, max_qty_1_ptpk, max_qty_2_ptpk,
             First_Quantity, Second_Quantity, First_Toll_rate, Second_Toll_rate, First_Unloading, Second_Unloading,
             max_qty_1_lead, max_qty_2_lead, First_city_lat, Second_city_lat, First_city_long, Second_city_long,
             new_destination_lead, Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM, Lead_diff, PTPK_diff_from_Ref_city1,
             COMMENT]]
        ref_dataframe11 = pd.DataFrame(ref_dataframe1,
                                       columns=["REF_CITY_CODE1", "REF_CITY_CODE2", "REF_CITY_NAME1", "REF_CITY_NAME2",
                                                "REF_CITY1_PTPK", "REF_CITY2_PTPK", "REF_QUANTITY1", "REF_QUANTITY2",
                                                "REF_TOLLRATE1", "REF_TOLLRATE2", "REF_UNLOADING1", "REF_UNLOADING2",
                                                "REF_LEAD1", "REF_LEAD2", "REF_LATITUDE1", "REF_LATITUDE2", "REF_LONG1",
                                                "REF_LONG2", "PROPOSED_LEAD", "PRED_PTPK", "PRED_BASE_FREIGHT",
                                                "PTPK_CHANGEperKM", "Lead_diff", "PTPK_diff_from_Ref_city1", "COMMENT"])

        ref_dataframe11.reset_index(drop=True, inplace=True)

    return ref_dataframe11

'''
taluka analysis: logic:3

'''


'''
scenario 1

'''


def scenario1(df, out, ref_dataframe11, df_logic3, PLANT, address1, DIRECT_STO, taluka, TRUCK_TYPE):
    #print("enter into scenario 1")
    new_destination_lead = out['Proposed_Lead'][0]
    max_qty_1_lead = float(df['Lead'][0])
    max_qty_2_lead = float(df['Lead'][1])

    max_qty_1_ptpk = df['PTPK'][0]
    max_qty_2_ptpk = df['PTPK'][1]

    max_qty_1_source_lat = df['Source_Lat'][0]
    max_qty_1_source_long = df['Source_Long'][0]
    max_qty_1_dest_lat = df['lat'][0]
    max_qty_1_dest_long = df['Long'][0]

    # get google distance of first city with source
    google_lead = df['Google_Dist'][0]
    lower_limit_lead = min(max_qty_1_lead, max_qty_2_lead) - abs(max_qty_1_lead - max_qty_2_lead) * 0.2
    upper_limit_lead = max(max_qty_1_lead, max_qty_2_lead) + abs(max_qty_1_lead - max_qty_2_lead) * 0.2

    if lower_limit_lead <= new_destination_lead <= upper_limit_lead:
        #print("first_condtion_satisfied")
        slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)
        Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)
        Pred_PTPK = round(Pred_PTPK, 2)

        Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
        COMMENT = "PTPK FOUND USING REF POINTS"
        PTPK_CHANGEperKM = (max_qty_1_ptpk - max_qty_2_ptpk) / (max_qty_1_lead - max_qty_2_lead)
        Lead_diff = (new_destination_lead - max_qty_1_lead)
        PTPK_diff_from_Ref_city1 = (Pred_PTPK - max_qty_1_ptpk)
        ref_dataframe11.loc[0] = [df['CITY_CODE'][0], df['CITY_CODE'][1], df["CITY_DESC"][0], df["CITY_DESC"][1],
                                  max_qty_1_ptpk, max_qty_2_ptpk,
                                  df['QUANTITY'][0], df['QUANTITY'][1], df['TOLL_RATE'][0], df['TOLL_RATE'][1],
                                  df['UNLOADING'][0], df['UNLOADING'][1],
                                  max_qty_1_lead, max_qty_2_lead, df['lat'][0], df['lat'][1], df['Long'][0],
                                  df['Long'][1],
                                  new_destination_lead, Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM, Lead_diff,
                                  PTPK_diff_from_Ref_city1, COMMENT]


    elif len(df) > 2:  # if there is only two points max qty lead and 2nd max qty lead will always be same
        #print("second_condition_satisfied")
        df1 = df.drop_duplicates(subset=["Lead"])
        lead_diff_max = abs(new_destination_lead - max(df1["Lead"]))
        lead_diff_min = abs(new_destination_lead - min(df1["Lead"]))
        if lead_diff_max < lead_diff_min:
            df1.sort_values(by="Lead", ascending=False, inplace=True)
        else:
            df1.sort_values(by="Lead", ascending=True, inplace=True)

        df1.reset_index(drop=True, inplace=True)
        coverage = 0
        i = 2
        while i != len(df1):
            #print("run_while_loop")
            #print(i)
            df_check = df1.head(i)
            max_lead = max(df_check["Lead"])
            min_lead = min(df_check["Lead"])
            if min_lead <= new_destination_lead <= max_lead:

                df_check.sort_values(by="QUANTITY", ascending=False, inplace=True)
                max_qty_1_lead = float(df_check['Lead'][0])
                max_qty_2_lead = float(df_check['Lead'][1])
                max_qty_1_ptpk = df_check['PTPK'][0]
                max_qty_2_ptpk = df_check['PTPK'][1]
                max_qty_1_source_lat = df_check['Source_Lat'][0]
                max_qty_1_source_long = df_check['Source_Long'][0]
                max_qty_1_dest_lat = df_check['lat'][0]
                max_qty_1_dest_long = df_check['Long'][0]
                slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)
                Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)
                Pred_PTPK = round(Pred_PTPK, 2)
                Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                COMMENT = "PTPK FOUND USING REF POINTS"
                PTPK_CHANGEperKM = (max_qty_1_ptpk - max_qty_2_ptpk) / (max_qty_1_lead - max_qty_2_lead)
                Lead_diff = (new_destination_lead - max_qty_1_lead)
                PTPK_diff_from_Ref_city1 = (Pred_PTPK - max_qty_1_ptpk)
                ref_dataframe11.loc[0] = [df_check['CITY_CODE'][0], df_check['CITY_CODE'][1], df_check["CITY_DESC"][0],
                                          df_check["CITY_DESC"][1], max_qty_1_ptpk, max_qty_2_ptpk,
                                          df_check['QUANTITY'][0], df_check['QUANTITY'][1], df_check['TOLL_RATE'][0],
                                          df_check['TOLL_RATE'][1], df_check['UNLOADING'][0], df_check['UNLOADING'][1],
                                          max_qty_1_lead, max_qty_2_lead, df_check['lat'][0], df_check['lat'][1],
                                          df_check['Long'][0], df_check['Long'][1],
                                          new_destination_lead, Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM,
                                          Lead_diff, PTPK_diff_from_Ref_city1, COMMENT]

                coverage = 1

            else:
                df_check.sort_values(by="QUANTITY", ascending=False, inplace=True)
                df_check.reset_index(drop=True, inplace=True)
                max_qty_1_lead = float(df_check['Lead'][0])
                max_qty_2_lead = float(df_check['Lead'][1])
                min_lead = min(df_check["Lead"])
                coverage = abs((max_qty_1_lead - max_qty_2_lead) / (new_destination_lead - min_lead))
                max_qty_1_ptpk = df_check['PTPK'][0]
                max_qty_2_ptpk = df_check['PTPK'][1]
                max_qty_1_source_lat = df_check['Source_Lat'][0]
                max_qty_1_source_long = df_check['Source_Long'][0]
                max_qty_1_dest_lat = df_check['lat'][0]
                max_qty_1_dest_long = df_check['Long'][0]
                slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)
                Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)
                Pred_PTPK = round(Pred_PTPK, 2)
                Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)
                COMMENT = "PTPK FOUND USING REF POINTS"
                PTPK_CHANGEperKM = (max_qty_1_ptpk - max_qty_2_ptpk) / (max_qty_1_lead - max_qty_2_lead)
                Lead_diff = (new_destination_lead - max_qty_1_lead)
                PTPK_diff_from_Ref_city1 = (Pred_PTPK - max_qty_1_ptpk)
                ref_dataframe11.loc[0] = [df_check['CITY_CODE'][0], df_check['CITY_CODE'][1], df_check["CITY_DESC"][0],
                                          df_check["CITY_DESC"][1], max_qty_1_ptpk, max_qty_2_ptpk,
                                          df_check['QUANTITY'][0], df_check['QUANTITY'][1], df_check['TOLL_RATE'][0],
                                          df_check['TOLL_RATE'][1], df_check['UNLOADING'][0], df_check['UNLOADING'][1],
                                          max_qty_1_lead, max_qty_2_lead, df_check['lat'][0], df_check['lat'][1],
                                          df_check['Long'][0], df_check['Long'][1],
                                          new_destination_lead, Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM,
                                          Lead_diff, PTPK_diff_from_Ref_city1, COMMENT]

                i = i + 1  # in order to take rows in recursive manner(first 2, then3, then 4 and so on)
            if coverage > 0.8:
                break
            #print("end_while_loop")
    elif (df_logic3.empty == False) & (len(df_logic3) != 1):
        #print("logic3_begins")
        Pred_PTPK = np.nan
        ref_dataframe11 = logic3(dispatchdata, PLANT, address1, DIRECT_STO, taluka, out, TRUCK_TYPE, Pred_PTPK,
                                 new_destination_lead, df_logic3, ref_dataframe11)

    else:
        #print("scenario4_starts")
        ref_dataframe11 = scenario4(dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, ref_dataframe11)

    return ref_dataframe11


'''
taluka analysis: logic:3

'''
'''
logic3_ratio

'''


def ratio_method(df11, dispatchdata, taluka, PLANT, DIRECT_STO, ref_dataframe11, out, TRUCK_TYPE):
    l = list(df11['TRUCK_TYPE'].unique())

    for i in range(len(l)):
        df = dispatchdata[(dispatchdata['Taluka_input'] == taluka) & (dispatchdata['DELVRY_PLANT'] == PLANT) & (
                dispatchdata['TRUCK_TYPE'] == l[i]) & (dispatchdata['Direct_STO'] == DIRECT_STO.upper())]
        df.sort_values(by='QUANTITY', ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df["Lead"] = df["Lead"].astype(float)
        if (df.empty == False) & (len(df) != 1):
            ref_other_tt = scenario1(df, out, ref_dataframe11, df_logic3)
            #print(l[i])
            if ref_other_tt["PRED_PTPK"][0] != np.nan:
                break
        else:
            continue

    dist_tt_lead = min(df["Lead"])
    dispatchdata_plant_x = dispatchdata[
        (dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == l[i]) & (
                dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (dispatchdata["Lead"] >= dist_tt_lead - 12.5)]
    dispatchdata_plant_y = dispatchdata[
        (dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (
                dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (dispatchdata["Lead"] >= dist_tt_lead - 12.5)]
    #print("enter into weighted average")
    Pred_PTPK_tt = ref_other_tt["PRED_PTPK"][0]
    other_trucktype = l[i]
    x = range(int(min(dispatchdata_plant_x["Lead"])), int(max(dispatchdata_plant_x["Lead"]) + 1))
    y = range(int(min(dispatchdata_plant_y["Lead"])), int(max(dispatchdata_plant_y["Lead"]) + 1))

    l = list(set(x) & set(y))
    dispatchdata_plant_x1 = dispatchdata_plant_x[
        (dispatchdata_plant_x["Lead"] >= min(l)) & (dispatchdata_plant_x["Lead"] <= max(l))]
    dispatchdata_plant_y1 = dispatchdata_plant_y[
        (dispatchdata_plant_y["Lead"] >= min(l)) & (dispatchdata_plant_y["Lead"] <= max(l))]

    # ratio
    dispatchdata_plant_x1["Product"] = dispatchdata_plant_x1["QUANTITY"] * dispatchdata_plant_x1[
        "PTPK"]
    dispatchdata_plant_y1["Product"] = dispatchdata_plant_y1["QUANTITY"] * dispatchdata_plant_y1[
        "PTPK"]

    WA1 = sum(dispatchdata_plant_x1["Product"]) / sum(dispatchdata_plant_x1["QUANTITY"])
    WA2 = sum(dispatchdata_plant_y1["Product"]) / sum(dispatchdata_plant_y1["QUANTITY"])
    Pred_PTPK = (WA1 / WA2) * Pred_PTPK_tt
    Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
    new_destination_lead = out["Proposed_Lead"][0]
    COMMENT = "PTPK_FOUND_USING_OTHER_TRUCKTYPE USING" + " " + other_trucktype
    PTPK_CHANGEperKM = (ref_other_tt['REF_CITY1_PTPK'][0] - ref_other_tt['REF_CITY2_PTPK'][0]) / (
            ref_other_tt['REF_LEAD1'][0] - ref_other_tt['REF_LEAD2'][0])
    Lead_diff = (new_destination_lead - ref_other_tt['REF_LEAD1'][0])
    PTPK_diff_from_Ref_city1 = (Pred_PTPK - ref_other_tt['REF_CITY1_PTPK'][0])

    ref_dataframe11.loc[0] = [ref_other_tt['REF_CITY_CODE1'][0], ref_other_tt['REF_CITY_CODE2'][0],
                              ref_other_tt["REF_CITY_NAME1"][0], ref_other_tt["REF_CITY_NAME2"][0],
                              ref_other_tt['REF_CITY1_PTPK'][0], ref_other_tt['REF_CITY2_PTPK'][0],
                              ref_other_tt['REF_QUANTITY1'][0], ref_other_tt['REF_QUANTITY2'][0],
                              ref_other_tt['REF_TOLLRATE1'][0], ref_other_tt['REF_TOLLRATE2'][0],
                              ref_other_tt['REF_UNLOADING1'][0], ref_other_tt['REF_UNLOADING2'][0],
                              ref_other_tt['REF_LEAD1'][0], ref_other_tt['REF_LEAD2'][0],
                              ref_other_tt['REF_LATITUDE1'][0], ref_other_tt['REF_LATITUDE2'][0],
                              ref_other_tt['REF_LONG1'][0], ref_other_tt['REF_LONG2'][0],
                              new_destination_lead, Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM, Lead_diff,
                              PTPK_diff_from_Ref_city1, COMMENT]

    return ref_dataframe11


def logic3(dispatchdata, PLANT, address1, DIRECT_STO, taluka, out, TRUCK_TYPE, Pred_PTPK, new_destination_lead,
           df_logic3, ref_dataframe11):
    # dispatchdata["Lead"]=dispatchdata["Lead"].astype(float)
    #print("logic3_starts")
    df11 = df_logic3[df_logic3["TRUCK_TYPE"] != str(TRUCK_TYPE)]
    df11_exist = df_logic3[
        df_logic3["TRUCK_TYPE"] == str(TRUCK_TYPE)]  # suppose 1106 does not exist the ratio will be nan

    if (df11.empty == False) & (df11_exist.empty == False):

        df11 = df_logic3[df_logic3["TRUCK_TYPE"] != str(TRUCK_TYPE)]
        df11_exist = df_logic3[
            df_logic3["TRUCK_TYPE"] == str(TRUCK_TYPE)]  # suppose 1106 does not exist the ratio will be nan
        df11['dist'] = np.nan
        df11.reset_index(drop=True, inplace=True)
        for i in range(len(df11)):
            #print(i)
            df11['dist'][i] = distance_matrix(out["New_destination_LAT"], out["New_destination_LONG"], df11["lat"][i],
                                              df11["Long"][i], key)

        df12 = df11[df11['dist'] == min(df11['dist'])]

        df12.reset_index(drop=True, inplace=True)
        dist_tt = df12['dist'][0]
        if ((dist_tt < 5) == True) & ((dist_tt <= np.round(out["Proposed_Lead"][0] * 0.03)) == True) & (
                df11_exist.empty == False):
            try:
                dist_tt_lead = df12["Lead"][0]

                dispatchdata_plant_x = dispatchdata[
                    (dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == df12["TRUCK_TYPE"][0]) & (
                            dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                            dispatchdata["Lead"] >= dist_tt_lead - 12.5)]
                dispatchdata_plant_y = dispatchdata[
                    (dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (
                            dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                            dispatchdata["Lead"] >= dist_tt_lead - 12.5)]

                #print("enter into weighted average")
                Pred_PTPK_tt = np.round(df12["PTPK"][0], 2)

                other_trucktype = df12["TRUCK_TYPE"][0]

                x = range(int(min(dispatchdata_plant_x["Lead"])), int(max(dispatchdata_plant_x["Lead"]) + 1))
                y = range(int(min(dispatchdata_plant_y["Lead"])), int(max(dispatchdata_plant_y["Lead"]) + 1))

                l = list(set(x) & set(y))

                dispatchdata_plant_x1 = dispatchdata_plant_x[
                    (dispatchdata_plant_x["Lead"] >= min(l)) & (dispatchdata_plant_x["Lead"] <= max(l))]
                dispatchdata_plant_y1 = dispatchdata_plant_y[
                    (dispatchdata_plant_y["Lead"] >= min(l)) & (dispatchdata_plant_y["Lead"] <= max(l))]

                # ratio
                dispatchdata_plant_x1["Product"] = dispatchdata_plant_x1["QUANTITY"] * dispatchdata_plant_x1[
                    "PTPK"]
                dispatchdata_plant_y1["Product"] = dispatchdata_plant_y1["QUANTITY"] * dispatchdata_plant_y1[
                    "PTPK"]

                WA1 = sum(dispatchdata_plant_x1["Product"]) / sum(dispatchdata_plant_x1["QUANTITY"])
                WA2 = sum(dispatchdata_plant_y1["Product"]) / sum(dispatchdata_plant_y1["QUANTITY"])

                Pred_PTPK = (WA1 / WA2) * Pred_PTPK_tt

                Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
                COMMENT = "PTPK_FOUND_USING_OTHER_TRUCKTYPE USING: " + df12["TRUCK_TYPE"][0]
                PTPK_CHANGEperKM = np.nan
                Lead_diff = (new_destination_lead - df12['REF_LEAD1'][0])
                PTPK_diff_from_Ref_city1 = (Pred_PTPK - df12['REF_CITY1_PTPK'][0])
                ref_dataframe11.loc[0] = [df12["CITY_CODE"][0], np.nan, df12['CITY_DESC'][0], np.nan, df12["PTPK"][0],
                                          np.nan,
                                          df12["QUANTITY"][0], np.nan, df12["TOLL_RATE"][0], np.nan,
                                          df12["UNLOADING"][0], np.nan,
                                          df12["Lead"][0], np.nan, df12["lat"][0], np.nan, df12["Long"][0], np.nan,
                                          out["Proposed_Lead"][0], Pred_PTPK, Pred_Base_Freight, PTPK_CHANGEperKM,
                                          Lead_diff, PTPK_diff_from_Ref_city1, COMMENT]
            except:
                try:
                    ref_dataframe11 = ratio_method(df11, dispatchdata, taluka, PLANT, DIRECT_STO, ref_dataframe11)

                except:
                    try:
                        ref_dataframe11 = scenario4(dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, ref_dataframe11)
                    except:
                        pass
        else:
            try:
                ref_dataframe11 = ratio_method(df11, dispatchdata, taluka, PLANT, DIRECT_STO, ref_dataframe11, out)
            except:
                ref_dataframe11 = scenario4(dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, ref_dataframe11)


    else:
        try:
            ref_dataframe11 = ratio_method(df11, dispatchdata, taluka, PLANT, DIRECT_STO, ref_dataframe11, out)

        except:
            ref_dataframe11 = scenario4(dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, ref_dataframe11)

    return ref_dataframe11


def ptpk_logic3(dispatchdata, PLANT, address1, DIRECT_STO, taluka, out, TRUCK_TYPE, Pred_PTPK, new_destination_lead):
    # dispatchdata["Lead"]=dispatchdata["Lead"].astype(float)
    # print("enter into logic 3")
    dispatchdata = slab_new1(dispatchdata)

    df1 = dispatchdata[(dispatchdata['Taluka_input'] == taluka) & (dispatchdata['DELVRY_PLANT'] == PLANT) & (
            dispatchdata['Direct_STO'] == DIRECT_STO.upper())]

    df1.sort_values(by='TRUCK_TYPE', ascending=True, inplace=True)

    if (df1.empty == False) & (len(df1) != 1) & (pd.isna(Pred_PTPK) == True):

        df11 = df1[df1["TRUCK_TYPE"] != str(TRUCK_TYPE)]
        df11_exist = df1[df1["TRUCK_TYPE"] == str(TRUCK_TYPE)]  # suppose 1106 does not exist the ratio will be nan
        df11['dist'] = np.nan
        df11.reset_index(drop=True, inplace=True)
        for i in range(len(df11)):
            # print(i)
            df11['dist'][i] = distance_matrix(out["New_destination_LAT"], out["New_destination_LONG"], df11["lat"][i],
                                              df11["Long"][i], key)

        df12 = df11[df11['dist'] == min(df11['dist'])]

        df12.reset_index(drop=True, inplace=True)
        dist_tt = df12['dist'][0]
        try:
            if ((dist_tt < 5) == True) & ((dist_tt <= np.round(out["Proposed_Lead"][0] * 0.03)) == True) & (
                    df11_exist.empty == False):

                dist_tt_lead = df12["Lead"][0]

                dispatchdata_plant_x = dispatchdata[
                    (dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == df12["TRUCK_TYPE"][0]) & (
                            dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                            dispatchdata["Lead"] >= dist_tt_lead - 12.5)]
                dispatchdata_plant_y = dispatchdata[
                    (dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (
                            dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                            dispatchdata["Lead"] >= dist_tt_lead - 12.5)]

                # print("enter into weighted average")
                Pred_PTPK_tt = np.round(df12["PTPK"][0], 2)

                other_trucktype = df12["TRUCK_TYPE"][0]

                #            dispatch_other_trucktype = dispatchdata[
                #                (dispatchdata["TRUCK_TYPE"] == other_trucktype) & (dispatchdata['Slab_new'] == out["Slab_new"][0])]
                #
                #            dispatch_pred_trucktype = dispatchdata[
                #                (dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (dispatchdata['Slab_new'] == out["Slab_new"][0])]

                x = range(int(min(dispatchdata_plant_x["Lead"])), int(max(dispatchdata_plant_x["Lead"]) + 1))
                y = range(int(min(dispatchdata_plant_y["Lead"])), int(max(dispatchdata_plant_y["Lead"]) + 1))

                l = list(set(x) & set(y))

                dispatchdata_plant_x1 = dispatchdata_plant_x[
                    (dispatchdata_plant_x["Lead"] >= min(l)) & (dispatchdata_plant_x["Lead"] <= max(l))]
                dispatchdata_plant_y1 = dispatchdata_plant_y[
                    (dispatchdata_plant_y["Lead"] >= min(l)) & (dispatchdata_plant_y["Lead"] <= max(l))]

                # ratio
                dispatchdata_plant_x1["Product"] = dispatchdata_plant_x1["QUANTITY"] * dispatchdata_plant_x1[
                    "PTPK"]
                dispatchdata_plant_y1["Product"] = dispatchdata_plant_y1["QUANTITY"] * dispatchdata_plant_y1[
                    "PTPK"]

                WA1 = sum(dispatchdata_plant_x1["Product"]) / sum(dispatchdata_plant_x1["QUANTITY"])
                WA2 = sum(dispatchdata_plant_y1["Product"]) / sum(dispatchdata_plant_y1["QUANTITY"])

                Pred_PTPK = (WA1 / WA2) * Pred_PTPK_tt

                Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)

                First_city_code = df12["CITY_CODE"][0]
                Second_city_code = np.nan
                First_city_name = df12['CITY_DESC'][0]
                Second_city_name = np.nan
                max_qty_1_ptpk = df12["PTPK"][0]
                max_qty_2_ptpk = np.nan
                First_Quantity = df12["QUANTITY"][0]
                Second_Quantity = np.nan
                First_Toll_rate = df12["TOLL_RATE"][0]
                Second_Toll_rate = np.nan
                First_Unloading = df12["UNLOADING"][0]
                Second_Unloading = np.nan
                max_qty_1_lead = df12["Lead"][0]
                max_qty_2_lead = np.nan
                First_city_lat = df12["lat"][0]
                Second_city_lat = np.nan
                First_city_long = df12["Long"][0]
                Second_city_long = np.nan
                new_destination_lead = out["Proposed_Lead"][0]
                COMMENT = "PTPK_FOUND_USING_OTHER_TRUCKTYPE USING: " + df12["TRUCK_TYPE"][0]


            else:
                # print("logic 3 else condition")
                df = dispatchdata[(dispatchdata['Taluka_input'] == taluka) & (dispatchdata['DELVRY_PLANT'] == PLANT) & (
                        dispatchdata['TRUCK_TYPE'] == df12['TRUCK_TYPE'][0]) & (
                                          dispatchdata['Direct_STO'] == DIRECT_STO.upper())]
                df.sort_values(by='QUANTITY', ascending=False, inplace=True)
                df.reset_index(drop=True, inplace=True)
                df["Lead"] = df["Lead"].astype(float)

                if df.empty == False:

                    max_qty_1_lead = float(df['Lead'][0])
                    max_qty_2_lead = float(df['Lead'][1])

                    max_qty_1_ptpk = df['PTPK'][0]
                    max_qty_2_ptpk = df['PTPK'][1]

                    max_qty_1_source_lat = df['Source_Lat'][0]
                    max_qty_1_source_long = df['Source_Long'][0]
                    max_qty_1_dest_lat = df['lat'][0]
                    max_qty_1_dest_long = df['Long'][0]

                    # get google distance of first city with source
                    google_lead = df['Google_Dist'][0]

                    # Correction for Google Lead
                    # new_destination_lead = new_destination_google_lead + (max_qty_1_lead-google_lead)
                    # new_destination_lead=71
                    # for coverage
                    lower_limit_lead = min(max_qty_1_lead, max_qty_2_lead) - abs(max_qty_1_lead - max_qty_2_lead) * 0.2
                    upper_limit_lead = max(max_qty_1_lead, max_qty_2_lead) + abs(max_qty_1_lead - max_qty_2_lead) * 0.2

                    if lower_limit_lead <= new_destination_lead <= upper_limit_lead:

                        slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)
                        First_city_code = df['CITY_CODE'][0]
                        Second_city_code = df['CITY_CODE'][1]

                        First_city_name = df["CITY_DESC"][0]
                        Second_city_name = df["CITY_DESC"][1]

                        First_Quantity = df['QUANTITY'][0]
                        Second_Quantity = df['QUANTITY'][1]

                        First_Toll_rate = df['TOLL_RATE'][0]
                        Second_Toll_rate = df['TOLL_RATE'][1]

                        First_Unloading = df['UNLOADING'][0]
                        Second_Unloading = df['UNLOADING'][1]

                        First_city_lat = df['lat'][0]
                        First_city_long = df['Long'][0]

                        Second_city_lat = df['lat'][1]
                        Second_city_long = df['Long'][1]
                        COMMENT = "PTPK_FOUND_THROUGH_REF_POINT_Of_Other_trucktype(scenario3)"

                        Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)
                        Pred_PTPK = np.round(Pred_PTPK, 2)

                        Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)


                    else:

                        median_lead = np.median(df['Lead'])

                        df_more = df[df['Lead'] >= median_lead]
                        df_less = df[df['Lead'] < median_lead]

                        df_more.reset_index(drop=True, inplace=True)
                        df_less.reset_index(drop=True, inplace=True)
                        max_lead_df_more = max(df_more["Lead"])
                        min_lead_df_more = min(df_more['Lead'])
                        max_lead_df_less = max(df_less['Lead'])
                        min_lead_df_less = min(df_less['Lead'])

                        # print("ma_more:", max_lead_df_more)
                        # print("min_more:", min_lead_df_more)
                        # print("max_less:", max_lead_df_less)
                        # print("min_less:", min_lead_df_less)
                        # print("new_destination_lead:", new_destination_lead)
                        if (len(df_more) > 1) & (len(df_less) > 1):
                            #
                            if min_lead_df_more <= new_destination_lead <= max_lead_df_more:

                                df_more.sort_values(by='QUANTITY', ascending=False, inplace=True)
                                df_more.reset_index(drop=True, inplace=True)
                                max_qty_1_lead = df_more['Lead'][0]
                                max_qty_2_lead = df_more['Lead'][1]

                                max_qty_1_ptpk = df_more['PTPK'][0]
                                max_qty_2_ptpk = df_more['PTPK'][1]

                                First_city_code = df_more['CITY_CODE'][0]
                                Second_city_code = df_more['CITY_CODE'][1]

                                First_city_name = df_more["CITY_DESC"][0]
                                Second_city_name = df_more["CITY_DESC"][1]

                                First_Quantity = df_more['QUANTITY'][0]
                                Second_Quantity = df_more['QUANTITY'][1]

                                First_Toll_rate = df_more['TOLL_RATE'][0]
                                Second_Toll_rate = df_more['TOLL_RATE'][1]

                                First_Unloading = df_more['UNLOADING'][0]
                                Second_Unloading = df_more['UNLOADING'][1]

                                First_city_lat = df_more['lat'][0]
                                First_city_long = df_more['Long'][0]

                                Second_city_lat = df_more['lat'][1]
                                Second_city_long = df_more['Long'][1]
                                COMMENT = "PTPK_FOUND_THROUGH_REF_POINT_OF_OTHERTRUCKTYPE"

                                slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                                Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                                Pred_PTPK = np.round(Pred_PTPK, 2)
                                Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)





                            elif min_lead_df_less <= new_destination_lead <= max_lead_df_less:
                                df_less.sort_values(by='QUANTITY', ascending=False, inplace=True)
                                df_less.reset_index(drop=True, inplace=True)
                                max_qty_1_lead = df_less['Lead'][0]
                                max_qty_2_lead = df_less['Lead'][1]

                                max_qty_1_ptpk = df_less['PTPK'][0]
                                max_qty_2_ptpk = df_less['PTPK'][1]

                                First_city_code = df_less['CITY_CODE'][0]
                                Second_city_code = df_less['CITY_CODE'][1]

                                First_city_name = df_less["CITY_DESC"][0]
                                Second_city_name = df_less["CITY_DESC"][1]

                                First_Quantity = df_less['QUANTITY'][0]
                                Second_Quantity = df_less['QUANTITY'][1]

                                First_Toll_rate = df_less['TOLL_RATE'][0]
                                Second_Toll_rate = df_less['TOLL_RATE'][1]

                                First_Unloading = df_less['UNLOADING'][0]
                                Second_Unloading = df_less['UNLOADING'][1]

                                First_city_lat = df_less['lat'][0]
                                First_city_long = df_less['Long'][0]

                                Second_city_lat = df_less['lat'][1]
                                Second_city_long = df_less['Long'][1]
                                COMMENT = "PTPK_FOUND_THROUGH_REF_POINT_OF_OTHERTRUCKTYPE"

                                slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                                Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                                Pred_PTPK = np.round(Pred_PTPK, 2)
                                Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)






                            else:
                                diff_max_more = abs(new_destination_lead - max_lead_df_more)
                                diff_min_more = abs(new_destination_lead - min_lead_df_more)
                                diff_max_less = abs(new_destination_lead - max_lead_df_less)
                                diff_min_less = abs(new_destination_lead - min_lead_df_less)

                                if min(diff_max_more, diff_min_more, diff_max_less, diff_min_less) == diff_max_more:
                                    df_more.sort_values(by='QUANTITY', ascending=False, inplace=True)
                                    df_more.reset_index(drop=True, inplace=True)
                                    max_qty_1_lead = df_more['Lead'][0]
                                    max_qty_2_lead = df_more['Lead'][1]

                                    max_qty_1_ptpk = df_more['PTPK'][0]
                                    max_qty_2_ptpk = df_more['PTPK'][1]

                                    First_city_code = df_more['CITY_CODE'][0]
                                    Second_city_code = df_more['CITY_CODE'][1]

                                    First_city_name = df_more["CITY_DESC"][0]
                                    Second_city_name = df_more["CITY_DESC"][1]

                                    First_Quantity = df_more['QUANTITY'][0]
                                    Second_Quantity = df_more['QUANTITY'][1]

                                    First_Toll_rate = df_more['TOLL_RATE'][0]
                                    Second_Toll_rate = df_more['TOLL_RATE'][1]

                                    First_Unloading = df_more['UNLOADING'][0]
                                    Second_Unloading = df_more['UNLOADING'][1]

                                    First_city_lat = df_more['lat'][0]
                                    First_city_long = df_more['Long'][0]

                                    Second_city_lat = df_more['lat'][1]
                                    Second_city_long = df_more['Long'][1]
                                    COMMENT = "PTPK_FOUND_THROUGH_REF_POINT_OF_OTHERTRUCKTYPE"

                                    slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                                    Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                                    Pred_PTPK = np.round(Pred_PTPK, 2)
                                    Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)


                                elif min(diff_max_more, diff_min_more, diff_max_less, diff_min_less) == diff_min_more:
                                    df_more.sort_values(by='QUANTITY', ascending=False, inplace=True)
                                    df_more.reset_index(drop=True, inplace=True)
                                    max_qty_1_lead = df_more['Lead'][0]
                                    max_qty_2_lead = df_more['Lead'][1]

                                    max_qty_1_ptpk = df_more['PTPK'][0]
                                    max_qty_2_ptpk = df_more['PTPK'][1]

                                    First_city_code = df_more['CITY_CODE'][0]
                                    Second_city_code = df_more['CITY_CODE'][1]

                                    First_city_name = df_more["CITY_DESC"][0]
                                    Second_city_name = df_more["CITY_DESC"][1]

                                    First_Quantity = df_more['QUANTITY'][0]
                                    Second_Quantity = df_more['QUANTITY'][1]

                                    First_Toll_rate = df_more['TOLL_RATE'][0]
                                    Second_Toll_rate = df_more['TOLL_RATE'][1]

                                    First_Unloading = df_more['UNLOADING'][0]
                                    Second_Unloading = df_more['UNLOADING'][1]

                                    First_city_lat = df_more['lat'][0]
                                    First_city_long = df_more['Long'][0]

                                    Second_city_lat = df_more['lat'][1]
                                    Second_city_long = df_more['Long'][1]
                                    COMMENT = "PTPK_FOUND_THROUGH_REF_POINT_OF_OTHERTRUCKTYPE"
                                    slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                                    Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                                    Pred_PTPK = np.round(Pred_PTPK, 2)
                                    Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)



                                else:
                                    df_less.sort_values(by='QUANTITY', ascending=False, inplace=True)
                                    df_less.reset_index(drop=True, inplace=True)
                                    max_qty_1_lead = df_less['Lead'][0]
                                    max_qty_2_lead = df_less['Lead'][1]

                                    max_qty_1_ptpk = df_less['PTPK'][0]
                                    max_qty_2_ptpk = df_less['PTPK'][1]

                                    First_city_code = df_less['CITY_CODE'][0]
                                    Second_city_code = df_less['CITY_CODE'][1]

                                    First_city_name = df_less["CITY_DESC"][0]
                                    Second_city_name = df_less["CITY_DESC"][1]

                                    First_Quantity = df_less['QUANTITY'][0]
                                    Second_Quantity = df_less['QUANTITY'][1]

                                    First_Toll_rate = df_less['TOLL_RATE'][0]
                                    Second_Toll_rate = df_less['TOLL_RATE'][1]

                                    First_Unloading = df_less['UNLOADING'][0]
                                    Second_Unloading = df_less['UNLOADING'][1]

                                    First_city_lat = df_less['lat'][0]
                                    First_city_long = df_less['Long'][0]

                                    Second_city_lat = df_less['lat'][1]
                                    Second_city_long = df_less['Long'][1]
                                    COMMENT = "PTPK_FOUND_THROUGH_REF_POINT_OF_OTHERTRUCKTYPE"

                                    slope = (max_qty_2_ptpk - max_qty_1_ptpk) / (max_qty_2_lead - max_qty_1_lead)

                                    Pred_PTPK = max_qty_1_ptpk + slope * (new_destination_lead - max_qty_1_lead)

                                    Pred_PTPK = np.round(Pred_PTPK, 2)
                                    Pred_Base_Freight = math.floor(Pred_PTPK * new_destination_lead)

                    if pd.isna(Pred_PTPK) == False:
                        dist_tt_lead = df12["Lead"][0]

                        dispatchdata_plant_x = dispatchdata[(dispatchdata["DELVRY_PLANT"] == PLANT) & (
                                dispatchdata["TRUCK_TYPE"] == df12["TRUCK_TYPE"][0]) & (
                                                                    dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                                                                    dispatchdata["Lead"] >= dist_tt_lead - 12.5)]
                        dispatchdata_plant_y = dispatchdata[(dispatchdata["DELVRY_PLANT"] == PLANT) & (
                                dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (
                                                                    dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                                                                    dispatchdata["Lead"] >= dist_tt_lead - 12.5)]

                        # print("enter into weighted average")
                        Pred_PTPK_tt = Pred_PTPK

                        dist_tt_lead = df12["Lead"][0]

                        dispatchdata_plant_x = dispatchdata[(dispatchdata["DELVRY_PLANT"] == PLANT) & (
                                dispatchdata["TRUCK_TYPE"] == df12["TRUCK_TYPE"][0]) & (
                                                                    dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                                                                    dispatchdata["Lead"] >= dist_tt_lead - 12.5)]
                        dispatchdata_plant_y = dispatchdata[(dispatchdata["DELVRY_PLANT"] == PLANT) & (
                                dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (
                                                                    dispatchdata["Lead"] <= dist_tt_lead + 12.5) & (
                                                                    dispatchdata["Lead"] >= dist_tt_lead - 12.5)]

                        # print("enter into weighted average")

                        other_trucktype = df12["TRUCK_TYPE"][0]

                        #            dispatch_other_trucktype = dispatchdata[
                        #                (dispatchdata["TRUCK_TYPE"] == other_trucktype) & (dispatchdata['Slab_new'] == out["Slab_new"][0])]
                        #
                        #            dispatch_pred_trucktype = dispatchdata[
                        #                (dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) & (dispatchdata['Slab_new'] == out["Slab_new"][0])]

                        x = range(int(min(dispatchdata_plant_x["Lead"])), int(max(dispatchdata_plant_x["Lead"]) + 1))
                        y = range(int(min(dispatchdata_plant_y["Lead"])), int(max(dispatchdata_plant_y["Lead"]) + 1))

                        l = list(set(x) & set(y))

                        dispatchdata_plant_x1 = dispatchdata_plant_x[
                            (dispatchdata_plant_x["Lead"] >= min(l)) & (dispatchdata_plant_x["Lead"] <= max(l))]
                        dispatchdata_plant_y1 = dispatchdata_plant_y[
                            (dispatchdata_plant_y["Lead"] >= min(l)) & (dispatchdata_plant_y["Lead"] <= max(l))]

                        # ratio
                        dispatchdata_plant_x1["Product"] = dispatchdata_plant_x1["QUANTITY"] * dispatchdata_plant_x1[
                            "PTPK"]
                        dispatchdata_plant_y1["Product"] = dispatchdata_plant_y1["QUANTITY"] * dispatchdata_plant_y1[
                            "PTPK"]

                        WA1 = sum(dispatchdata_plant_x1["Product"]) / sum(dispatchdata_plant_x1["QUANTITY"])
                        WA2 = sum(dispatchdata_plant_y1["Product"]) / sum(dispatchdata_plant_y1["QUANTITY"])

                        Pred_PTPK = (WA1 / WA2) * Pred_PTPK_tt

                        Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)

                        First_city_code = df12["CITY_CODE"][0]
                        Second_city_code = np.nan
                        First_city_name = df12['CITY_DESC'][0]
                        Second_city_name = np.nan
                        max_qty_1_ptpk = df12["PTPK"][0]
                        max_qty_2_ptpk = np.nan
                        First_Quantity = df12["QUANTITY"][0]
                        Second_Quantity = np.nan
                        First_Toll_rate = df12["TOLL_RATE"][0]
                        Second_Toll_rate = np.nan
                        First_Unloading = df12["UNLOADING"][0]
                        Second_Unloading = np.nan
                        max_qty_1_lead = df12["Lead"][0]
                        max_qty_2_lead = np.nan
                        First_city_lat = df12["lat"][0]
                        Second_city_lat = np.nan
                        First_city_long = df12["Long"][0]
                        Second_city_long = np.nan
                        new_destination_lead = out["Proposed_Lead"][0]
                        COMMENT = "PTPK_FOUND_USING_OTHER_TRUCKTYPE USING" + " " + df12["TRUCK_TYPE"][0]
                    else:
                        ref_dataframe = scenario4(Pred_PTPK, dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, PLANT,hierarchydata)
                        First_city_code = ref_dataframe[0]
                        Second_city_code = ref_dataframe[1]
                        First_city_name = ref_dataframe[2]
                        Second_city_name = ref_dataframe[3]
                        max_qty_1_ptpk = ref_dataframe[4]
                        max_qty_2_ptpk = ref_dataframe[5]
                        First_Quantity = ref_dataframe[6]
                        Second_Quantity = ref_dataframe[7]
                        First_Toll_rate = ref_dataframe[8]
                        Second_Toll_rate = ref_dataframe[9]
                        First_Unloading = ref_dataframe[10]
                        Second_Unloading = ref_dataframe[11]
                        max_qty_1_lead = ref_dataframe[12]
                        max_qty_2_lead = ref_dataframe[13]
                        First_city_lat = ref_dataframe[14]
                        Second_city_lat = ref_dataframe[15]
                        First_city_long = ref_dataframe[16]
                        Second_city_long = ref_dataframe[17]
                        new_destination_lead = ref_dataframe[18]
                        Pred_PTPK = ref_dataframe[19]
                        Pred_Base_Freight = ref_dataframe[20]
                        COMMENT = ref_dataframe[21]





        except:
            Pred_PTPK = np.nan
            ref_dataframe = scenario4(Pred_PTPK, dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, PLANT,hierarchydata)
            First_city_code = ref_dataframe[0]
            Second_city_code = ref_dataframe[1]
            First_city_name = ref_dataframe[2]
            Second_city_name = ref_dataframe[3]
            max_qty_1_ptpk = ref_dataframe[4]
            max_qty_2_ptpk = ref_dataframe[5]
            First_Quantity = ref_dataframe[6]
            Second_Quantity = ref_dataframe[7]
            First_Toll_rate = ref_dataframe[8]
            Second_Toll_rate = ref_dataframe[9]
            First_Unloading = ref_dataframe[10]
            Second_Unloading = ref_dataframe[11]
            max_qty_1_lead = ref_dataframe[12]
            max_qty_2_lead = ref_dataframe[13]
            First_city_lat = ref_dataframe[14]
            Second_city_lat = ref_dataframe[15]
            First_city_long = ref_dataframe[16]
            Second_city_long = ref_dataframe[17]
            new_destination_lead = ref_dataframe[18]
            Pred_PTPK = ref_dataframe[19]
            Pred_Base_Freight = ref_dataframe[20]
            COMMENT = ref_dataframe[21]


    elif (pd.isna(Pred_PTPK) == True):
        ref_dataframe = scenario4(Pred_PTPK, dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, PLANT,hierarchydata)
        First_city_code = ref_dataframe[0]
        Second_city_code = ref_dataframe[1]
        First_city_name = ref_dataframe[2]
        Second_city_name = ref_dataframe[3]
        max_qty_1_ptpk = ref_dataframe[4]
        max_qty_2_ptpk = ref_dataframe[5]
        First_Quantity = ref_dataframe[6]
        Second_Quantity = ref_dataframe[7]
        First_Toll_rate = ref_dataframe[8]
        Second_Toll_rate = ref_dataframe[9]
        First_Unloading = ref_dataframe[10]
        Second_Unloading = ref_dataframe[11]
        max_qty_1_lead = ref_dataframe[12]
        max_qty_2_lead = ref_dataframe[13]
        First_city_lat = ref_dataframe[14]
        Second_city_lat = ref_dataframe[15]
        First_city_long = ref_dataframe[16]
        Second_city_long = ref_dataframe[17]
        new_destination_lead = ref_dataframe[18]
        Pred_PTPK = ref_dataframe[19]
        Pred_Base_Freight = ref_dataframe[20]
        COMMENT = ref_dataframe[21]

    else:
        # print("no ref point")
        First_city_code = np.nan
        Second_city_code = np.nan
        First_city_name = np.nan
        Second_city_name = np.nan
        max_qty_1_ptpk = np.nan
        max_qty_2_ptpk = np.nan
        First_Quantity = np.nan
        Second_Quantity = np.nan
        First_Toll_rate = np.nan
        Second_Toll_rate = np.nan
        First_Unloading = np.nan
        Second_Unloading = np.nan
        max_qty_1_lead = np.nan
        max_qty_2_lead = np.nan
        First_city_lat = np.nan
        Second_city_lat = np.nan
        First_city_long = np.nan
        Second_city_long = np.nan
        new_destination_lead = out["Proposed_Lead"][0]
        Pred_PTPK = Pred_PTPK
        Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
        COMMENT = "NO_PTPK_FOUND (There is no data from same plant to same taluka)"

    return First_city_code, Second_city_code, First_city_name, Second_city_name, max_qty_1_ptpk, max_qty_2_ptpk, First_Quantity, Second_Quantity, First_Toll_rate, Second_Toll_rate, First_Unloading, Second_Unloading, max_qty_1_lead, max_qty_2_lead, First_city_lat, Second_city_lat, First_city_long, Second_city_long, new_destination_lead, Pred_PTPK, Pred_Base_Freight, COMMENT


'''
scenario 4

'''

def scenario4(Pred_PTPK, dispatchdata, TRUCK_TYPE, DIRECT_STO, out, taluka, PLANT,hierarchydata):
    max_lead = out["Proposed_Lead"][0] + out["Proposed_Lead"][0] * 0.15
    min_lead = out["Proposed_Lead"][0] - out["Proposed_Lead"][0] * 0.15
    df = dispatchdata[(dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata["TRUCK_TYPE"] == str(TRUCK_TYPE)) &
                      (dispatchdata["Direct_STO"] == DIRECT_STO.upper()) & (dispatchdata['Lead'] >= min_lead) & (
                              dispatchdata['Lead'] <= max_lead)]
    try:
        district=hierarchydata["district_code"][0] #district_code
        depot=hierarchydata["depot_code"][0]
    except:
        district=np.nan
        depot=np.nan
#    df['lat'] = df['lat'].astype(float)
#    df['Long'] = df['Long'].astype(float)
#    df.reset_index(drop=True,inplace=True)
#    #source = Point(float(df['Source_Lat'][0]), float(df['Source_Long'][0]))  # Plant Lat-Long
#    new_dest=Point(float(out['New_destination_LAT'][0]), float(out['New_destination_LONG'][0])) 
#    newdest_cir = new_dest.buffer(radius)  # Circle taking new dest as center and Radius as 10% of proposed lead
#    df['flag']=0
#    for i in range(len(df)):
#        print(i)
#        if Point(df['lat'][i], df['Long'][i]).within(newdest_cir):
#            df['flag'][i]=1
#        else:
#            df['flag'][i]=0
        
    df_filter=df.copy()
    
    df_same=df_filter[df_filter['Taluka_input']==taluka]
    df_same.reset_index(drop=True,inplace=True)
    df_same_district=df_filter[df_filter['district_code']==district]#district_code
    df_same_depot=df_filter[df_filter['depot_code']==depot]
    if len(df_filter)>0:
        if len(df_same)>0:
            df_same["lead_diff"]=abs(df_same["Lead"]-out["Proposed_Lead"][0])
            df_same.sort_values(['lead_diff'], ascending=True,inplace=True)
            df_same.reset_index(drop=True,inplace=True)
            Pred_PTPK=np.round(df_same["PTPK"][0],2)
            Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
            
            First_city_code = np.nan
            Second_city_code = np.nan
            First_city_name = np.nan
            Second_city_name = np.nan
            max_qty_1_ptpk = np.nan
            max_qty_2_ptpk = np.nan
            First_Quantity = np.nan
            Second_Quantity = np.nan
            First_Toll_rate = np.nan
            Second_Toll_rate = np.nan
            First_Unloading = np.nan
            Second_Unloading = np.nan
            max_qty_1_lead = np.nan
            max_qty_2_lead = np.nan
            First_city_lat = np.nan
            Second_city_lat = np.nan
            First_city_long = np.nan
            Second_city_long = np.nan
            new_destination_lead = out["Proposed_Lead"][0]
            COMMENT = "PTPK FOUND USING SIMILAR LEAD FROM THE SAME PLANT(SCENARIO 4) USING CITY CODE,CITY_DESC AND TALUKA:"+df_same["CITY_CODE"][0]+" "+df_same["CITY_DESC"][0]+" "+df_same["I2_TALUKA_DESC"][0]
        elif len(df_same_district)>0:
            df_same_district["lead_diff"]=abs(df_same_district["Lead"]-out["Proposed_Lead"][0])
            df_same_district.sort_values(['lead_diff'], ascending=True,inplace=True)
            df_same_district.reset_index(drop=True,inplace=True)
            Pred_PTPK=np.round(df_same_district["PTPK"][0],2)
            Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
            
            First_city_code = np.nan
            Second_city_code = np.nan
            First_city_name = np.nan
            Second_city_name = np.nan
            max_qty_1_ptpk = np.nan
            max_qty_2_ptpk = np.nan
            First_Quantity = np.nan
            Second_Quantity = np.nan
            First_Toll_rate = np.nan
            Second_Toll_rate = np.nan
            First_Unloading = np.nan
            Second_Unloading = np.nan
            max_qty_1_lead = np.nan
            max_qty_2_lead = np.nan
            First_city_lat = np.nan
            Second_city_lat = np.nan
            First_city_long = np.nan
            Second_city_long = np.nan
            new_destination_lead = out["Proposed_Lead"][0]
            COMMENT = "PTPK FOUND USING SIMILAR LEAD FROM THE SAME PLANT(SCENARIO 4) USING CITY CODE,CITY_DESC AND DISTRICT:"+df_same_district["CITY_CODE"][0]+" "+df_same_district["CITY_DESC"][0]+" "+df_same_district["DISTRICT_DESC"][0]
        elif len(df_same_depot)>0:
            df_same_depot["lead_diff"]=abs(df_same_depot["Lead"]-out["Proposed_Lead"][0])
            df_same_depot.sort_values(['lead_diff'], ascending=True,inplace=True)
            df_same_depot.reset_index(drop=True,inplace=True)
            Pred_PTPK=np.round(df_same_depot["PTPK"][0],2)
            Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
            
            First_city_code = np.nan
            Second_city_code = np.nan
            First_city_name = np.nan
            Second_city_name = np.nan
            max_qty_1_ptpk = np.nan
            max_qty_2_ptpk = np.nan
            First_Quantity = np.nan
            Second_Quantity = np.nan
            First_Toll_rate = np.nan
            Second_Toll_rate = np.nan
            First_Unloading = np.nan
            Second_Unloading = np.nan
            max_qty_1_lead = np.nan
            max_qty_2_lead = np.nan
            First_city_lat = np.nan
            Second_city_lat = np.nan
            First_city_long = np.nan
            Second_city_long = np.nan
            new_destination_lead = out["Proposed_Lead"][0]
            COMMENT = "PTPK FOUND USING SIMILAR LEAD FROM THE SAME PLANT(SCENARIO 4) USING CITY CODE,CITY_DESC AND DEPOT:"+df_same_depot["CITY_CODE"][0]+" "+df_same_depot["CITY_DESC"][0]+" "+df_same_depot["depot_desc"][0]
          
        else:
            df_filter["lead_diff"]=abs(df_filter["Lead"]-out["Proposed_Lead"][0])
            df_filter.sort_values(['lead_diff'], ascending=True,inplace=True)
            df_filter.reset_index(drop=True,inplace=True)
            Pred_PTPK=np.round(df_filter["PTPK"][0],2)
            Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
            
            First_city_code = np.nan
            Second_city_code = np.nan
            First_city_name = np.nan
            Second_city_name = np.nan
            max_qty_1_ptpk = np.nan
            max_qty_2_ptpk = np.nan
            First_Quantity = np.nan
            Second_Quantity = np.nan
            First_Toll_rate = np.nan
            Second_Toll_rate = np.nan
            First_Unloading = np.nan
            Second_Unloading = np.nan
            max_qty_1_lead = np.nan
            max_qty_2_lead = np.nan
            First_city_lat = np.nan
            Second_city_lat = np.nan
            First_city_long = np.nan
            Second_city_long = np.nan
            new_destination_lead = out["Proposed_Lead"][0]
            COMMENT = "PTPK FOUND USING SIMILAR LEAD FROM THE SAME PLANT(SCENARIO 4) USING CITY CODE,CITY_DESC AND TALUKA:"+df_filter["CITY_CODE"][0]+" "+df_filter["CITY_DESC"][0]+" "+df_filter["I2_TALUKA_DESC"][0]
         
    else:#change
        Pred_Base_Freight = np.round(Pred_PTPK * out["Proposed_Lead"][0], 2)
        First_city_code = np.nan
        Second_city_code = np.nan
        First_city_name = np.nan
        Second_city_name = np.nan
        max_qty_1_ptpk = np.nan
        max_qty_2_ptpk = np.nan
        First_Quantity = np.nan
        Second_Quantity = np.nan
        First_Toll_rate = np.nan
        Second_Toll_rate = np.nan
        First_Unloading = np.nan
        Second_Unloading = np.nan
        max_qty_1_lead = np.nan
        max_qty_2_lead = np.nan
        First_city_lat = np.nan
        Second_city_lat = np.nan
        First_city_long = np.nan
        Second_city_long = np.nan
        new_destination_lead = out["Proposed_Lead"][0]
        COMMENT = "NO PTPK FOUND"

    return First_city_code, Second_city_code, First_city_name, Second_city_name, max_qty_1_ptpk, max_qty_2_ptpk, First_Quantity, Second_Quantity, First_Toll_rate, Second_Toll_rate, First_Unloading, Second_Unloading, max_qty_1_lead, max_qty_2_lead, First_city_lat, Second_city_lat, First_city_long, Second_city_long, new_destination_lead, Pred_PTPK, Pred_Base_Freight, COMMENT


######################################################################################################


'''
nearest point function new logic 20-07 (nearest dataframe)

'''


def nearest_all(PLANT, TRUCK_TYPE, DIRECT_STO, dispatchdata, out, LAT, LONG, dist):
    new_destination_google_lead = dist
    new_destination_lat = LAT

    new_destination_long = LONG

    df = dispatchdata[(dispatchdata['DELVRY_PLANT'] == PLANT) & (dispatchdata['TRUCK_TYPE'] == str(TRUCK_TYPE)) & (
            dispatchdata['Direct_STO'] == DIRECT_STO.upper())]

    df.reset_index(drop=True, inplace=True)
    if len(df) != 0:
        df['lat'] = df['lat'].astype(float)
        df['Long'] = df['Long'].astype(float)
        source = Point(float(df['Source_Lat'][0]), float(df['Source_Long'][0]))  # Plant Lat-Long
        new_dest = Point(LAT, LONG)  # New destination Lat-Long
        dist1 = source.distance(new_dest)  # Distance between Source and New-Destination

        plant_newdest_cir = source.buffer(
            dist1)  # Circle taking Source as center and Radius as distance (Source-New_Destination)
        newdest_cir = new_dest.buffer(dist1)  # Cirlce considering New-Destination as center
        Area_greater = newdest_cir.difference(plant_newdest_cir)  # for distance more than New-Destination
        Area_smaller = newdest_cir.intersection(plant_newdest_cir)  # for distance less than New-Destination

        # Points in Area_smaller
        points_smaller = MultiPoint([Point(df['lat'][i], df['Long'][i]) for i in range(len(df)) if
                                     Point(df['lat'][i], df['Long'][i]).within(Area_smaller)])
        points_greater = MultiPoint([Point(df['lat'][i], df['Long'][i]) for i in range(len(df)) if
                                     Point(df['lat'][i], df['Long'][i]).within(Area_greater)])

        try:
            # Smallest Point
            point_smallest = nearest_points(new_dest, points_smaller)[1]
            df_smaller = df[df['lat'] == point_smallest.x]
            df_smaller.reset_index(drop=True, inplace=True)
            df_smaller1 = [[df_smaller['CITY_DESC'][0], df_smaller['I2_TALUKA_DESC'][0], df_smaller['Lead'][0],
                            df_smaller['Google_Dist'][0], df_smaller['PTPK'][0], df_smaller['Base.freight'][0],
                            df_smaller['QUANTITY'][0], df_smaller['TOLL_RATE'][0], df_smaller['UNLOADING'][0],
                            df_smaller['lat'][0], df_smaller['Long'][0]]]

            Nearest_smaller_point = pd.DataFrame(df_smaller1,
                                                 columns=["NEAREST_SMALLER_CITY_NAME", "NEAREST_SMALLER_TALUKA_NAME",
                                                          "NEAREST_SMALLER_LEAD", "NEAREST_SMALLER_Google_Dist",
                                                          "NEAREST_SMALLER_PTPK", "NEAREST_SMALLER_BASE_FREIGHT",
                                                          "NEAREST_SMALLER_QUANTITY", "NEAREST_SMALLER_TOLL",
                                                          "NEAREST_SMALLER_UNLOADING", "NEAREST_SMALLER_lat",
                                                          "NEAREST_SMALLER_long"])

        except:
            df_smaller1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

            Nearest_smaller_point = pd.DataFrame(df_smaller1,
                                                 columns=["NEAREST_SMALLER_CITY_NAME", "NEAREST_SMALLER_TALUKA_NAME",
                                                          "NEAREST_SMALLER_LEAD", "NEAREST_SMALLER_Google_Dist",
                                                          "NEAREST_SMALLER_PTPK", "NEAREST_SMALLER_BASE_FREIGHT",
                                                          "NEAREST_SMALLER_QUANTITY", "NEAREST_SMALLER_TOLL",
                                                          "NEAREST_SMALLER_UNLOADING", "NEAREST_SMALLER_lat",
                                                          "NEAREST_SMALLER_long"])

        try:
            point_greatest = nearest_points(new_dest, points_greater)[1]
            df_greater = df[df["lat"] == point_greatest.x]
            df_greater.reset_index(drop=True, inplace=True)
            df_greater1 = [[df_greater['CITY_DESC'][0], df_greater['I2_TALUKA_DESC'][0], df_greater['Lead'][0],
                            df_greater['Google_Dist'][0], df_greater['PTPK'][0], df_greater['Base.freight'][0],
                            df_greater['QUANTITY'][0], df_greater['TOLL_RATE'][0], df_greater['UNLOADING'][0],
                            df_greater['lat'][0], df_greater['Long'][0]]]

            Nearest_greater_point = pd.DataFrame(df_greater1,
                                                 columns=["NEAREST_GREATER_CITY_NAME", "NEAREST_GREATER_TALUKA_NAME",
                                                          "NEAREST_GREATER_LEAD", "NEAREST_GREATER_Google_Dist",
                                                          "NEAREST_GREATER_PTPK", "NEAREST_GREATER_BASE_FREIGHT",
                                                          "NEAREST_GREATER_QUANTITY", "NEAREST_GREATER_TOLL",
                                                          "NEAREST_GREATER_UNLOADING", "NEAREST_GREATER_lat",
                                                          "NEAREST_GREATER_long"])
        except:
            df_greater1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

            Nearest_greater_point = pd.DataFrame(df_greater1,
                                                 columns=["NEAREST_GREATER_CITY_NAME", "NEAREST_GREATER_TALUKA_NAME",
                                                          "NEAREST_GREATER_LEAD", "NEAREST_GREATER_Google_Dist",
                                                          "NEAREST_GREATER_PTPK", "NEAREST_GREATER_BASE_FREIGHT",
                                                          "NEAREST_GREATER_QUANTITY", "NEAREST_GREATER_TOLL",
                                                          "NEAREST_GREATER_UNLOADING", "NEAREST_GREATER_lat",
                                                          "NEAREST_GREATER_long"])

        nearest_point = pd.concat([Nearest_greater_point, Nearest_smaller_point], axis=1)
        nearest_point.reset_index(drop=True, inplace=True)
    else:
        df_smaller1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

        Nearest_smaller_point = pd.DataFrame(df_smaller1,
                                             columns=["NEAREST_SMALLER_CITY_NAME", "NEAREST_SMALLER_TALUKA_NAME",
                                                      "NEAREST_SMALLER_LEAD", "NEAREST_SMALLER_Google_Dist",
                                                      "NEAREST_SMALLER_PTPK", "NEAREST_SMALLER_BASE_FREIGHT",
                                                      "NEAREST_SMALLER_QUANTITY", "NEAREST_SMALLER_TOLL",
                                                      "NEAREST_SMALLER_UNLOADING", "NEAREST_SMALLER_lat",
                                                      "NEAREST_SMALLER_long"])

        df_greater1 = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

        Nearest_greater_point = pd.DataFrame(df_greater1,
                                             columns=["NEAREST_GREATER_CITY_NAME", "NEAREST_GREATER_TALUKA_NAME",
                                                      "NEAREST_GREATER_LEAD", "NEAREST_GREATER_Google_Dist",
                                                      "NEAREST_GREATER_PTPK", "NEAREST_GREATER_BASE_FREIGHT",
                                                      "NEAREST_GREATER_QUANTITY", "NEAREST_GREATER_TOLL",
                                                      "NEAREST_GREATER_UNLOADING", "NEAREST_GREATER_lat",
                                                      "NEAREST_GREATER_long"])

        nearest_point = pd.concat([Nearest_greater_point, Nearest_smaller_point], axis=1)
        nearest_point.reset_index(drop=True, inplace=True)

    return nearest_point


#################################################################################################

#################################################################################################


'''
similarity features_extraction 

'''
gmaps = googlemaps.Client(key)


def Plain_Hilly_Per(elev_list, cut_off=350):
    total_len = len(elev_list)
    count = 0
    for i in range(total_len):
        if elev_list[i] >= 350:
            count += 1
    Hilly_Per = count / total_len
    Plain_Per = 1 - Hilly_Per

    return Plain_Per * 100, Hilly_Per * 100


'''
feature extraction

'''

NH_c = ["NH", "Hwy", "Highway", "HIGHWAY", "Ring", "ring", "RING", "HWY", "hwy", "highway", "AH", "Asian Highway"]
SH_c = ["SH"]


def feature_extraction(data, waypoints):
    global gmap_api_count
    cols = ['mean_ele', 'median_ele', 'max_ele', 'min_ele', 'range_ele', 'std_ele', 'kurtosis_ele', 'skewness_ele',
            'NH_Per', 'SH_Per', 'oth_Per', 'Plain_Per', 'Hilly_Per']
    temp = pd.DataFrame(columns=cols, index=range(len(data)))

    data.reset_index(drop=True, inplace=True)

    for i in range(len(data)):

        # print(i)
        source = (data['Source_Lat'][i], data['Source_Long'][i])
        destination = (data['Latitude'][i], data['Longitude'][i])

        try:

            # Get the Direction
            # ================New=========================
            if waypoints.size != 0:
                wpt = []
                for l in range(len(waypoints)):
                    wpt.append("via:" + str(waypoints[l][0]) + "," + str(waypoints[l][1]))

                # Get the Direction
                check1 = gmaps.directions(source, destination, waypoints=wpt)

            else:
                if map_data:
                    try:
                        check1 = map_data['elev_url'].get(str((source, destination)))
                    except KeyError as kex:
                        check1 = gmaps.directions(source, destination)
                        gmap_api_count = gmap_api_count + 1
                else:
                    check1 = gmaps.directions(source, destination)
            # ===============End==============================




                gmap_api_count = gmap_api_count + 1
                map_data_result['elev_url'][str((source, destination))] = check1

            step_len = len(check1[0]['legs'][0]['steps'])

            df = pd.DataFrame()

            for j in range(step_len):
                # print("step_len:",j)
                df.loc[j, 'lat'] = check1[0]['legs'][0]['steps'][j]['end_location']['lat']
                df.loc[j, 'lng'] = check1[0]['legs'][0]['steps'][j]['end_location']['lng']
                df.loc[j, 'distance'] = check1[0]['legs'][0]['steps'][j]['distance']['value']
                df.loc[j, 'comment'] = check1[0]['legs'][0]['steps'][j]['html_instructions']

            for k in range(len(df)):
                if any(ext in df['comment'][k] for ext in NH_c):
                    df.loc[k, 'NH_flag'] = 1
                else:
                    df.loc[k, 'NH_flag'] = 0
                if any(ext in df['comment'][k] for ext in SH_c):
                    df.loc[k, 'SH_flag'] = 1
                else:
                    df.loc[k, 'SH_flag'] = 0

            total_dist = check1[0]['legs'][0]['distance']['value']
            non_NH_dist = df.groupby(['NH_flag'])['distance'].sum()[0.0]
            non_SH_dist = df.groupby(['SH_flag'])['distance'].sum()[0.0]

            NH_dist = total_dist - non_NH_dist
            SH_dist = total_dist - non_SH_dist
            oth_dist = total_dist - NH_dist - SH_dist

            NH_Per = NH_dist / total_dist
            SH_Per = SH_dist / total_dist
            oth_Per = oth_dist / total_dist

            # print(step_len)

            # Extract Elevation data
            if map_data:
                try:
                    elevation_data = map_data['elevation_extraction'][str(([[float(str(data['Source_Lat'][i])),
                                                                             float(str(data['Source_Long'][i]))],
                                                                            [float(str(data['Latitude'][i])),
                                                                             float(str(data['Longitude'][i]))]],
                                                                           max(step_len, 2)))]
                except Exception as kex:
                    elevation_data = gmaps.elevation_along_path(
                        [[float(str(data['Source_Lat'][i])), float(str(data['Source_Long'][i]))],
                         [float(str(data['Latitude'][i])), float(str(data['Longitude'][i]))]], samples=max(step_len, 2))
                    gmap_api_count = gmap_api_count + 1
            else:
                elevation_data = gmaps.elevation_along_path(
                    [[float(str(data['Source_Lat'][i])), float(str(data['Source_Long'][i]))],
                     [float(str(data['Latitude'][i])), float(str(data['Longitude'][i]))]], samples=max(step_len, 2))
                gmap_api_count = gmap_api_count + 1
                map_data_result['elevation_extraction'][str(([[float(str(data['Source_Lat'][i])),
                                                               float(str(data['Source_Long'][i]))],
                                                              [float(str(data['Latitude'][i])),
                                                               float(str(data['Longitude'][i]))]],
                                                             max(step_len, 2)))] = elevation_data

            # Elevation feature extraction

            elev_list = []
            elev_list1 = []
            elev_list2 = [0]
            for l in range(len(elevation_data)):
                elev_list1.append(elevation_data[l]['elevation'])
                elev_list2.append(elevation_data[l]['elevation'])
            elev_list2 = elev_list2[:-1]
            elev_list = list(np.array(elev_list1) - np.array(elev_list2))
            elev_list[0] = 0

            mean_ele = statistics.mean(elev_list)
            median_ele = statistics.median(elev_list)
            std_ele = statistics.stdev(elev_list)
            kurtosis_ele = scipy.stats.kurtosis(elev_list)
            skewness_ele = scipy.stats.skew(elev_list)
            min_ele = min(elev_list)
            max_ele = max(elev_list)
            range_ele = max_ele - min_ele
            Plain_Per, Hilly_Per = Plain_Hilly_Per(elev_list)

            #########################change################################################

            source = [[float(data['Source_Lat'][i]), float(data['Source_Long'][i])]]
            destination = [[data['Latitude'][i], data['Longitude'][i]]]
            waypts = waypoints
            waypts = list(waypts)
            total_route = source + waypts + destination

            # Get the distance
            distance_wayp = []
            elevation = []

            # approximate radius of earth in km
            R = 6373.0

            for n in range(1, len(total_route)):
                lat1 = radians(total_route[n - 1][0])
                lon1 = radians(total_route[n - 1][1])
                lat2 = radians(total_route[n][0])
                lon2 = radians(total_route[n][1])

                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                distance_wayp.append(R * c)

            Hilly_Per = []
            for m in range(1, len(total_route)):
                dist = distance_wayp[m - 1]
                nos_ele = max(2, int(dist / 10))
                ele = gmaps.elevation_along_path([total_route[m - 1], total_route[m]], samples=nos_ele)
                elex = [x['elevation'] for x in ele]
                Hilly_Per.append(np.sum(np.array(elex) > 350) / nos_ele)
                # Use np.diff instead of np.array for comparing elevation with last elevation

            Hilly_Per = (np.sum(np.multiply(Hilly_Per, distance_wayp)) / np.sum(distance_wayp)) * 100
            Plain_Per = 100 - Hilly_Per
            mean_ele = np.nan
            median_ele = np.nan
            std_ele = np.nan
            kurtosis_ele = np.nan
            skewness_ele = np.nan
            min_ele = np.nan
            max_ele = np.nan
            range_ele = np.nan
            ##################################################################################

            temp.loc[i, "NH_Per"] = NH_Per * 100
            temp.loc[i, "SH_Per"] = SH_Per * 100
            temp.loc[i, "oth_Per"] = oth_Per * 100
            temp.loc[i, "mean_ele"] = mean_ele
            temp.loc[i, "median_ele"] = median_ele
            temp.loc[i, "std_ele"] = std_ele
            temp.loc[i, "kurtosis_ele"] = kurtosis_ele
            temp.loc[i, "skewness_ele"] = skewness_ele
            temp.loc[i, "min_ele"] = min_ele
            temp.loc[i, "max_ele"] = max_ele
            temp.loc[i, "range_ele"] = range_ele
            temp.loc[i, "Plain_Per"] = Plain_Per
            temp.loc[i, "Hilly_Per"] = Hilly_Per

        except:
            temp.loc[i, :] = np.nan

    df = pd.concat([data, temp], axis=1, ignore_index=True)

    df.columns = list(data.columns) + cols
    return df


##############################################################################################

'''

similarity algorithm (similarity dataframe)

'''


#
#
def simi_algorithm(simi_data, rc1, DIRECT_STO, map_dataframe, out, dispatchdata, taluka, PLANT):
    # simi_data = simi_data1.merge(simi_data2,on=['PLANT','CITY_CODE'],how='left')
    simi_data.fillna(value=0, inplace=True)
    dispatchdata.rename(columns={"avg_total_restriction_time": "total_restriction_time"}, inplace=True)
    # simi_data['Total_Restriction_time'] = simi_data['Time_atentry'] + simi_data['Time_atenroute'] + simi_data['Time_atdestinstion']
    # keep_cols = ['PLANT', 'CITY_CODE', 'TRUCK_TYPE', 'Direct_STO','mean_ele', 'median_ele', 'max_ele', 'min_ele','range_ele', 'sd_ele', 'kurtosis_ele', 'skewness_ele','NH_Per','SH_Per', 'Other_Per', 'Lead', 'PTPK', 'Plain_Per','Hilly_Per', 'Slab','CLUSTER_FLAG', 'UNION_FLAG','Total_Restriction_time']
    keep_cols = ['PLANT', 'CITY_CODE', 'TRUCK_TYPE', 'Direct_STO', 'NH_Per', 'SH_Per', 'Other_Per', 'Lead', 'PTPK',
                 'Plain_Per', 'Hilly_Per', 'Slab', 'total_restriction_time', 'QUANTITY', 'I2_TALUKA_DESC']  # CHANGE
    comp_cols = ['NH_Per', 'SH_Per', 'Plain_Per', 'Hilly_Per', 'total_restriction_time']

    # comp_cols = ['NH_Per', 'SH_Per', 'Plain_Per', 'Hilly_Per']
    simi_data = simi_data[keep_cols]

    Total_Restriction_time = dispatchdata[dispatchdata['Taluka_input'] == taluka]
    Total_Restriction_time.reset_index(drop=True, inplace=True)
    try:
        Total_Restriction_time = Total_Restriction_time["total_restriction_time"][0]
        rc1['total_restriction_time'] = Total_Restriction_time
    except:
        rc1['total_restriction_time'] = np.nan

    if rc1['NH_Per'][0] < 15:
        rc1['SH_Per'][0] = rc1['SH_Per'][0] + rc1['NH_Per'][0]
        rc1['NH_Per'][0] = 0

    elif rc1['SH_Per'][0] < 15:

        rc1['NH_Per'][0] = rc1['SH_Per'][0] + rc1['NH_Per'][0]
        rc1['SH_Per'][0] = 0

    elif rc1['Plain_Per'][0] < 15:
        rc1['Hilly_Per'][0] = rc1['Hilly_Per'][0] + rc1['Plain_Per'][0]
        rc1['Plain_Per'][0] = 0

    elif rc1['Hilly_Per'][0] < 15:
        rc1['Plain_Per'][0] = rc1['Hilly_Per'][0] + rc1['Plain_Per'][0]
        rc1['Hilly_Per'][0] = 0

    df = simi_data.copy()
    df['Type'] = df['PLANT'] + "-" + df['TRUCK_TYPE'].astype(str) + "-" + df['Direct_STO']
    # df['Type'] = df['TRUCK_TYPE'].astype(str) + "-" + df['Direct_STO']

    # scaling_cols = ['mean_ele','median_ele', 'max_ele', 'min_ele', 'range_ele', 'sd_ele','kurtosis_ele', 'skewness_ele', 'NH_Per', 'SH_Per', 'Other_Per','Plain_Per', 'Hilly_Per','Total_Restriction_time']

    rc1["Direct_STO"] = DIRECT_STO
    # rc1["Total_Restriction_time"]=0
    # rc1["Key"] = rc1['Plnt'].astype(str) + rc1['Destination'] + rc1['Truck_Type'].astype(str) + rc1[
    #     'Direct_STO'].astype(str)

    # key = rc1["Key"][0]
    # plant = int(rc1['Plnt'][0])
    truck_type = str(rc1['TRUCK_TYPE'][0])
    cust_type = rc1['Direct_STO'][0]
    new_destination_lead = map_dataframe['PROPOSED_LEAD'][0]

    max_lead = new_destination_lead * 1.1
    min_lead = new_destination_lead * 0.9

    simi_data["Lead"] = simi_data["Lead"].astype(float)

    df = simi_data[(simi_data["PLANT"] == PLANT) & (simi_data['TRUCK_TYPE'] == truck_type) & (
            simi_data['Direct_STO'] == cust_type.upper()) & (
                           simi_data['Lead'] >= min_lead) & (simi_data['Lead'] <= max_lead)]
    df.reset_index(drop=True, inplace=True)

    min_vals = (rc1[comp_cols] * 0.7).to_dict()
    max_vals = (rc1[comp_cols] * 1.3).to_dict()

    # for k in max_vals.keys():
    #     if max_vals[k][0] <= 0.0:
    #         max_vals[k][0] = 5
    # for k in min_vals.keys():
    #     if min_vals[k][0] == 0.0:
    #         min_vals[k][0] = -0.1

    # filter_dict = {'mean_ele':lambda x:x.between(min_vals['mean_ele'][0],max_vals['mean_ele'][0]),'sd_ele':lambda x:x.between(min_vals['sd_ele'][0],max_vals['sd_ele'][0]),'NH_Per':lambda x:x.between(min_vals['NH_Per'][0],max_vals['NH_Per'][0]),'SH_Per':lambda x:x.between(min_vals['SH_Per'][0],max_vals['SH_Per'][0]),'Other_Per':lambda x:x.between(min_vals['Other_Per'][0],max_vals['Other_Per'][0]),'Plain_Per':lambda x:x.between(min_vals['Plain_Per'][0],max_vals['Plain_Per'][0]),'Hilly_Per':lambda x:x.between(min_vals['Hilly_Per'][0],max_vals['Hilly_Per'][0]),'Total_Restriction_time':lambda x:x.between(min_vals['Total_Restriction_time'][0],max_vals['Total_Restriction_time'][0])}

    filter_dict = {'NH_Per': lambda x: x.between(min_vals['NH_Per'][0], max_vals['NH_Per'][0]),
                   'SH_Per': lambda x: x.between(min_vals['SH_Per'][0], max_vals['SH_Per'][0]),
                   'Plain_Per': lambda x: x.between(min_vals['Plain_Per'][0], max_vals['Plain_Per'][0]),
                   'Hilly_Per': lambda x: x.between(min_vals['Hilly_Per'][0], max_vals['Hilly_Per'][0]),
                   'total_restriction_time': lambda x: x.between(min_vals['total_restriction_time'][0],
                                                                 max_vals['total_restriction_time'][0])}

    # scale = StandardScaler()

    # scaling_cols = list(filter_dict.keys())
    key_df = rc1

    # Filtering to keep 70% for key features

    for ky in ['NH_Per', 'SH_Per', 'Plain_Per', 'Hilly_Per']:
        if key_df.loc[0, ky] <= 15:
            max_vals[ky][0] = 15
            min_vals[ky][0] = 0

    # if key_df.loc[0, "total_restriction_time"] <= 4:
    #     max_vals["total_restriction_time"][0] = 4
    #     min_vals["total_restriction_time"][0] = 0

    comp_df = df[df.apply(filter_dict).sum(axis=1) == len(filter_dict)]
    comp_df.reset_index(drop=True, inplace=True)
    # print("print df: ", df)
    # print("print comp_df: ", comp_df)

    if len(comp_df) != 0:

        # print("first_condition")
        #        comp_df1=comp_df.copy()
        #        # Scaling the features
        #        comp_df_scaled = scale.fit_transform(comp_df1[scaling_cols])
        #        key_df_scaled = scale.transform(key_df[scaling_cols])
        #
        #
        #        similarity_list = []
        #        for i in range(len(comp_df)):
        #            similarity_list.append(abs(cosine_similarity(key_df_scaled.reshape(1,-1),comp_df_scaled[i].reshape(1,-1))[0][0]))
        #
        #        comp_df1['Similarity_value'] = similarity_list
        #
        #        comp_df1.sort_values("Similarity_value",ascending = False, inplace = True)
        #
        #        comp_df2=comp_df1.head(5)
        #        key_df["Predicted PTPK"]=min(comp_df2["PTPK"])
        #
        comp_df1 = comp_df.sort_values(by=['PTPK'])[0:5]
        comp_df1.reset_index(drop=True, inplace=False)
        key_df["Predicted PTPK"] = min(comp_df1["PTPK"])
        key_df1 = key_df.copy()
        key_df1["Lead"] = out["Proposed_Lead"][0]
        key_df1["Slab"] = out["Slab_new"][0]
        key_df1["QUANTITY"] = np.nan  # CHANGE
        key_df1 = key_df1[
            ["DELVRY_PLANT", "CITY_DESC", "TRUCK_TYPE", "Direct_STO", "NH_Per", "SH_Per", "oth_Per", "Lead",
             "Predicted PTPK", "Plain_Per", "Hilly_Per", "Slab_new", "total_restriction_time", "QUANTITY",
             "I2_TALUKA_DESC"]]  # CHANGE
        key_df1.rename(
            columns={"DELVRY_PLANT": "PLANT", "oth_Per": "Other_Per", "Predicted PTPK": "PTPK", "Slab_new": "Slab"},
            inplace=True)
        dispatch = dispatchdata[["CITY_CODE", "CITY_DESC"]]
        dispatch.drop_duplicates(keep="first", inplace=True)

        comp_df1 = comp_df1.merge(dispatch, how="left", on="CITY_CODE")
        comp_df1["CITY_CODE"] = comp_df1["CITY_DESC"]
        del comp_df1["CITY_DESC"]
        comp_df1.rename(columns={"CITY_CODE": "CITY_DESC"}, inplace=True)
        comp_df2 = pd.concat([key_df1, comp_df1], ignore_index=True)
    else:
        # print("third_condition")
        comp_df2 = [[np.nan, np.nan, "No_similar_path_found"]]
        comp_df2 = pd.DataFrame(comp_df2, columns=["PLANT", "CITY_CODE", "Similarity_values"])

    return comp_df2, key_df


''' if does not get simi result'''


def direction(PLANT, dispatchdata, simi_data, out, taluka, DIRECT_STO, TRUCK_TYPE, rc1):
    gmaps = googlemaps.Client("AIzaSyB8jQ2IZkGZSwShnXXPNulvAqb5Sq5WMuA")
    new_destination_lead = out['Proposed_Lead'][0]
    max_lead = new_destination_lead * 1.2
    min_lead = new_destination_lead * 0.8
    key_df1 = rc1[
        ["DELVRY_PLANT", "CITY_DESC", "TRUCK_TYPE", "Direct_STO", "NH_Per", "SH_Per", "oth_Per", "Proposed_Lead",
         "Plain_Per", "Hilly_Per", "Slab_new", "I2_TALUKA_DESC"]]
    key_df1.rename(columns={"oth_Per": "Other_Per", "Proposed_Lead": "Lead"}, inplace=True)
    key_df1['PTPK'] = np.nan
    key_df1['total_restriction_time'] = np.nan
    key_df1['QUANTITY'] = np.nan
    key_df1["NH_Per"] = np.nan
    key_df1["SH_Per"] = np.nan
    key_df1["Other_Per"] = np.nan
    key_df1["Plain_Per"] = np.nan
    key_df1["Hilly_Per"] = np.nan
    key_df1["SH_Per"] = np.nan
    key_df1["total_restriction_time"] = np.nan

    source = (out['Source_Lat'][0], out['Source_Long'][0])
    destination = (out['New_destination_LAT'][0], out['New_destination_LONG'][0])
    # Get the Direction
    check1 = gmaps.directions(source, destination)
    step_len = len(check1[0]['legs'][0]['steps'])

    rc2 = pd.DataFrame()
    for j in range(step_len):
        #print("step_len:", j)
        rc2.loc[j, 'lat'] = check1[0]['legs'][0]['steps'][j]['end_location']['lat']
        rc2.loc[j, 'lng'] = check1[0]['legs'][0]['steps'][j]['end_location']['lng']

    df = dispatchdata[(dispatchdata["DELVRY_PLANT"] == PLANT) & (dispatchdata['TRUCK_TYPE'] == str(TRUCK_TYPE)) & (
            dispatchdata['Direct_STO'] == DIRECT_STO.upper()) & (
                              dispatchdata['Lead'] >= min_lead) & (dispatchdata['Lead'] <= max_lead)]

    df.dropna(subset=['lat'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    if len(df) > 0:

        for i in range(len(df)):
            #print(i)
            source = (df['Source_Lat'][i], df['Source_Long'][i])
            destination = (df['lat'][i], df['Long'][i])
            # Get the Direction
            check1 = gmaps.directions(source, destination)
            step_len = len(check1[0]['legs'][0]['steps'])
            df_latlng = pd.DataFrame()
            for j in range(step_len):
                #print("step_len:", j)
                df_latlng.loc[j, 'lat'] = check1[0]['legs'][0]['steps'][j]['end_location']['lat']
                df_latlng.loc[j, 'lng'] = check1[0]['legs'][0]['steps'][j]['end_location']['lng']

            exp_data = rc2.values
            num_data = df_latlng.values

            track1 = LineString([[p[0], p[1]] for p in exp_data])
            track2 = LineString([[p[0], p[1]] for p in num_data])

            track1_buffer = track1.buffer(.02)

            match = track1_buffer.intersection(track2)

            df.loc[i, 'simi_matching_per'] = match.length / max(track1.length, track2.length)
        df1 = df[df['simi_matching_per'] >= 0.7]
        if len(df1) > 0:
            df1["NH_Per"] = np.nan
            df1["SH_Per"] = np.nan
            df1["Other_Per"] = np.nan
            df1["Plain_Per"] = np.nan
            df1["Hilly_Per"] = np.nan
            df1["SH_Per"] = np.nan
            df1["total_restriction_time"] = np.nan
            df1 = df1[["DELVRY_PLANT", "CITY_DESC", "TRUCK_TYPE", "Direct_STO", "NH_Per", "SH_Per", "Other_Per", "Lead",
                       "PTPK", "Plain_Per", "Hilly_Per", "Slab_new", "total_restriction_time", "QUANTITY",
                       "I2_TALUKA_DESC"]]
            key_df1 = key_df1[
                ["DELVRY_PLANT", "CITY_DESC", "TRUCK_TYPE", "Direct_STO", "NH_Per", "SH_Per", "Other_Per", "Lead",
                 "PTPK", "Plain_Per", "Hilly_Per", "Slab_new", "total_restriction_time", "QUANTITY", "I2_TALUKA_DESC"]]
            key_df1['PTPK'] = min(df1['PTPK'])
            key_df1['TRUCK_TYPE'] = str(key_df1['TRUCK_TYPE'][0])
            key_df1['Slab_new'] = str(key_df1['Slab_new'][0])
            simi_df1 = pd.concat([key_df1, df1], axis=0)
            simi_df1.rename(columns={"DELVRY_PLANT": "PLANT", "Slab_new": "Slab"}, inplace=True)
            simi_df1.reset_index(drop=True, inplace=True)
            similarity_predicted_ptpk = simi_df1['PTPK'][0]
        else:
            simi_df1 = [[np.nan, np.nan, "No_similar_path_found"]]
            simi_df1 = pd.DataFrame(key_df1, columns=["PLANT", "CITY_CODE", "Similarity_values"])
            similarity_predicted_ptpk = "No suggested PTPK"
    else:
        simi_df1 = [[np.nan, np.nan, "No_similar_path_found"]]
        simi_df1 = pd.DataFrame(key_df1, columns=["PLANT", "CITY_CODE", "Similarity_values"])
        similarity_predicted_ptpk = "No suggested PTPK"

    return simi_df1, similarity_predicted_ptpk



#####################################################################################################


'''
output function

'''


def Output_function(PLANT, PLANT_NAME, TALUKA, TRUCK_TYPE, DIRECT_STO, address1, LAT, LONG, similarity, dispatchdata,
                    hierarchydata, taluka, Lead, waypoints):
    LATANDLONG = Geocode_latlong(address1, key)  # if address is not numeric then, that means lat is NA

    LAT = LATANDLONG[0]  # then by geocode_latlong lat and long can be found corresponging to address
    # print(LAT)
    LONG = LATANDLONG[1]
    # print(LONG)

    LATLONG = [[LAT, LONG]]
    LATLONG1 = pd.DataFrame(LATLONG, columns=["New_destination_LAT", "New_destination_LONG"])
    out = pd.concat([Plant_Lat_Long(PLANT, bf), LATLONG1], axis=1)  # cbind plant name plant lat long and dest lat long

    dist = distance_matrix1(out["Source_Lat"], out["Source_Long"], out["New_destination_LAT"],
                           out["New_destination_LONG"], key, waypoints)  # find out the distance between source lat source long

    distance = [[dist]]
    distance = pd.DataFrame(distance, columns=["DISTANCE_SOURCE_NEWDESTINATION"])
    out = pd.concat([out, distance], axis=1)
    out["Comment_lead"] = np.nan

    nearest_point = nearest_all(PLANT, TRUCK_TYPE, DIRECT_STO, dispatchdata, out, LAT, LONG, dist)
    nearest_comment = np.nan
    Pred_PTPK = np.nan

    if (pd.isna(nearest_point["NEAREST_GREATER_CITY_NAME"][0]) == False) & (pd.isna(
            nearest_point["NEAREST_SMALLER_CITY_NAME"][0]) == False):

        # find out distance between new destination and nearest points

        dist1 = distance_matrix(out["New_destination_LAT"], out["New_destination_LONG"],
                                nearest_point["NEAREST_GREATER_lat"][0], nearest_point["NEAREST_GREATER_long"][0], key)

        dist2 = distance_matrix(out["New_destination_LAT"], out["New_destination_LONG"],
                                nearest_point["NEAREST_SMALLER_lat"][0], nearest_point["NEAREST_SMALLER_long"][0], key)

        if dist1 < dist2:

            # check if dist1 is less than 5 km and less than 3 percent of new destination lead

            if ((dist1 < 5) == True) & ((dist1 <= dist * 0.03) == True):

                Pred_PTPK = np.round(nearest_point["NEAREST_GREATER_PTPK"][0], 2)
                nearest_comment = nearest_point["NEAREST_GREATER_CITY_NAME"][0]
            else:
                Pred_PTPK = np.nan


        elif dist1 > dist2:

            if ((dist2 < 5) == True) & ((dist2 <= dist * 0.03) == True):

                Pred_PTPK = np.round(nearest_point["NEAREST_SMALLER_PTPK"][0], 2)  # change
                nearest_comment = nearest_point["NEAREST_SMALLER_CITY_NAME"][0]
            else:
                Pred_PTPK = np.nan


    elif (pd.isna(nearest_point["NEAREST_GREATER_CITY_NAME"][0]) == False) & (pd.isna(
            nearest_point["NEAREST_SMALLER_CITY_NAME"][0]) == True):

        dist1 = distance_matrix(out["New_destination_LAT"], out["New_destination_LONG"],
                                nearest_point["NEAREST_GREATER_lat"][0], nearest_point["NEAREST_GREATER_long"][0], key)

        if ((dist1 < 5) == True) & ((dist1 <= dist * 0.03) == True):

            Pred_PTPK = np.round(nearest_point["NEAREST_GREATER_PTPK"][0], 2)  # change
            nearest_comment = nearest_point["NEAREST_GREATER_CITY_NAME"][0]
        else:
            Pred_PTPK = np.nan


    elif (pd.isna(nearest_point["NEAREST_GREATER_CITY_NAME"][0]) == True) & (pd.isna(

            nearest_point["NEAREST_SMALLER_CITY_NAME"][0]) == False):

        dist2 = distance_matrix(out["New_destination_LAT"], out["New_destination_LONG"],
                                nearest_point["NEAREST_SMALLER_lat"][0], nearest_point["NEAREST_SMALLER_long"][0], key)

        if ((dist2 < 5) == True) & ((dist2 <= dist * 0.03) == True):

            Pred_PTPK = np.round(nearest_point["NEAREST_SMALLER_PTPK"][0], 2)  # change
            nearest_comment = nearest_point["NEAREST_SMALLER_CITY_NAME"][0]
        else:
            Pred_PTPK = np.nan


    else:

        Pred_PTPK = np.nan

    if pd.isna(Lead)==True:
        out = lead_proposed(PLANT, taluka, LAT, LONG,DIRECT_STO, dispatchdata, dist,out)
    else:
        out.loc[0,"Proposed_Lead"]=Lead
        out.loc[0,"Comment_lead"]="Lead is given by the user"

    # out = lead_proposed(PLANT, taluka, LAT, LONG, DIRECT_STO, dispatchdata, dist, out)

    ref_data_frame = PTPK_pred_TalukaAnalysis1(taluka, PLANT, TRUCK_TYPE, DIRECT_STO, out, dispatchdata, nearest_point,
                                               Pred_PTPK, nearest_comment, hierarchydata, address1=address1)
    REF_NEAREST = pd.concat([ref_data_frame, nearest_point], axis=1)
    max_newdest_lead = REF_NEAREST["PROPOSED_LEAD"][0] + REF_NEAREST["PROPOSED_LEAD"][0] * 0.20
    min_newdest_lead = REF_NEAREST["PROPOSED_LEAD"][0] - REF_NEAREST["PROPOSED_LEAD"][0] * 0.20
    #
    if (REF_NEAREST["NEAREST_GREATER_LEAD"][0] <= max_newdest_lead) & (
            REF_NEAREST["NEAREST_SMALLER_LEAD"][0] >= min_newdest_lead):
        REF_NEAREST = REF_NEAREST.copy()

    elif ((REF_NEAREST["NEAREST_GREATER_LEAD"][0] >= max_newdest_lead) | (
            pd.isna(REF_NEAREST["NEAREST_GREATER_LEAD"][0]))) & (
            (REF_NEAREST["NEAREST_SMALLER_LEAD"][0] >= min_newdest_lead) | (
            pd.isna(REF_NEAREST["NEAREST_SMALLER_LEAD"][0]))):
        REF_NEAREST["NEAREST_GREATER_CITY_NAME"] = np.nan
        REF_NEAREST["NEAREST_GREATER_TALUKA_NAME"] = np.nan
        REF_NEAREST["NEAREST_GREATER_LEAD"] = np.nan
        REF_NEAREST["NEAREST_GREATER_Google_Dist"] = np.nan
        REF_NEAREST["NEAREST_GREATER_PTPK"] = np.nan
        REF_NEAREST["NEAREST_GREATER_BASE_FREIGHT"] = np.nan
        REF_NEAREST["NEAREST_GREATER_QUANTITY"] = np.nan
        REF_NEAREST["NEAREST_GREATER_TOLL"] = np.nan
        REF_NEAREST["NEAREST_GREATER_UNLOADING"] = np.nan
        REF_NEAREST["NEAREST_GREATER_lat"] = np.nan
        REF_NEAREST["NEAREST_GREATER_long"] = np.nan

    elif ((REF_NEAREST["NEAREST_GREATER_LEAD"][0] <= max_newdest_lead) | (
            pd.isna(REF_NEAREST["NEAREST_GREATER_LEAD"][0]))) & (
            (REF_NEAREST["NEAREST_SMALLER_LEAD"][0] <= min_newdest_lead) | (
            pd.isna(REF_NEAREST["NEAREST_SMALLER_LEAD"][0]))):
        # print("yes")
        REF_NEAREST["NEAREST_SMALLER_CITY_NAME"][0] = np.nan
        REF_NEAREST["NEAREST_SMALLER_TALUKA_NAME"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_LEAD"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_Google_Dist"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_PTPK"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_BASE_FREIGHT"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_QUANTITY"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_TOLL"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_UNLOADING"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_lat"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_long"] = np.nan


    else:
        REF_NEAREST["NEAREST_GREATER_CITY_NAME"] = np.nan
        REF_NEAREST["NEAREST_GREATER_TALUKA_NAME"] = np.nan
        REF_NEAREST["NEAREST_GREATER_LEAD"] = np.nan
        REF_NEAREST["NEAREST_GREATER_Google_Dist"] = np.nan
        REF_NEAREST["NEAREST_GREATER_PTPK"] = np.nan
        REF_NEAREST["NEAREST_GREATER_BASE_FREIGHT"] = np.nan
        REF_NEAREST["NEAREST_GREATER_QUANTITY"] = np.nan
        REF_NEAREST["NEAREST_GREATER_TOLL"] = np.nan
        REF_NEAREST["NEAREST_GREATER_UNLOADING"] = np.nan
        REF_NEAREST["NEAREST_GREATER_lat"] = np.nan
        REF_NEAREST["NEAREST_GREATER_long"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_CITY_NAME"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_TALUKA_NAME"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_LEAD"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_Google_Dist"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_PTPK"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_BASE_FREIGHT"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_QUANTITY"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_TOLL"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_UNLOADING"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_lat"] = np.nan
        REF_NEAREST["NEAREST_SMALLER_long"] = np.nan

    REFERENCE_DATAFRAME1 = [
        [ref_data_frame["REF_CITY_NAME1"][0], ref_data_frame["REF_CITY1_PTPK"][0], ref_data_frame["REF_LEAD1"][0],
         ref_data_frame["REF_QUANTITY1"][0], ref_data_frame["REF_TOLLRATE1"][0], ref_data_frame["REF_UNLOADING1"][0]]]

    REFERENCE_DATAFRAME11 = pd.DataFrame(REFERENCE_DATAFRAME1,
                                         columns=["CITY_NAME", "PTPK", "Lead", "QUANTITY", "Toll", "Unloading"])

    REFERENCE_DATAFRAME2 = [
        [ref_data_frame["REF_CITY_NAME2"][0], ref_data_frame["REF_CITY2_PTPK"][0], ref_data_frame["REF_LEAD2"][0],
         ref_data_frame["REF_QUANTITY2"][0], ref_data_frame["REF_TOLLRATE2"][0], ref_data_frame["REF_UNLOADING2"][0]]]

    REFERENCE_DATAFRAME21 = pd.DataFrame(REFERENCE_DATAFRAME2,
                                         columns=["CITY_NAME", "PTPK", "Lead", "QUANTITY", "Toll", "Unloading"])

    REFERENCE_DATAFRAME = pd.concat([REFERENCE_DATAFRAME11, REFERENCE_DATAFRAME21], axis=0)
    REFERENCE_DATAFRAME.reset_index(drop=True, inplace=True)

    NEAREST_GREATER1 = [[REF_NEAREST["NEAREST_GREATER_CITY_NAME"][0], REF_NEAREST["NEAREST_GREATER_TALUKA_NAME"][0],
                         REF_NEAREST["NEAREST_GREATER_LEAD"][0], REF_NEAREST["NEAREST_GREATER_Google_Dist"][0],
                         REF_NEAREST["NEAREST_GREATER_PTPK"][0], REF_NEAREST["NEAREST_GREATER_QUANTITY"][0],
                         REF_NEAREST["NEAREST_GREATER_TOLL"][0], REF_NEAREST["NEAREST_GREATER_UNLOADING"][0]]]
    NEAREST_GREATER11 = pd.DataFrame(NEAREST_GREATER1,
                                     columns=["CITY_NAME", "TALUKA_NAME", "LEAD", "GOOGLE_DIST", "PTPK", "QUANTITY",
                                              "TOLL", "UNLOADING"])

    NEAREST_SMALLER1 = [[REF_NEAREST["NEAREST_SMALLER_CITY_NAME"][0], REF_NEAREST["NEAREST_SMALLER_TALUKA_NAME"][0],
                         REF_NEAREST["NEAREST_SMALLER_LEAD"][0], REF_NEAREST["NEAREST_SMALLER_Google_Dist"][0],
                         REF_NEAREST["NEAREST_SMALLER_PTPK"][0], REF_NEAREST["NEAREST_SMALLER_QUANTITY"][0],
                         REF_NEAREST["NEAREST_SMALLER_TOLL"][0], REF_NEAREST["NEAREST_SMALLER_UNLOADING"][0]]]
    NEAREST_SMALLER11 = pd.DataFrame(NEAREST_SMALLER1,
                                     columns=["CITY_NAME", "TALUKA_NAME", "LEAD", "GOOGLE_DIST", "PTPK", "QUANTITY",
                                              "TOLL", "UNLOADING"])

    NEAREST_DATAFRAME = pd.concat([NEAREST_GREATER11, NEAREST_SMALLER11], axis=0)
    NEAREST_DATAFRAME.reset_index(drop=True, inplace=True)
    map_df = [[PLANT, PLANT_NAME, out["Source_Lat"][0], out["Source_Long"][0], address1, out["New_destination_LAT"][0],
               out["New_destination_LONG"][0], out['DISTANCE_SOURCE_NEWDESTINATION'][0],
               REF_NEAREST['REF_CITY_CODE1'][0], REF_NEAREST["REF_CITY_CODE2"][0], REF_NEAREST["REF_LATITUDE1"][0],
               REF_NEAREST["REF_LONG1"][0], REF_NEAREST["REF_LATITUDE2"][0], REF_NEAREST["REF_LONG2"][0],
               REF_NEAREST["NEAREST_GREATER_lat"][0], REF_NEAREST["NEAREST_GREATER_long"][0],
               REF_NEAREST["NEAREST_SMALLER_lat"][0], REF_NEAREST["NEAREST_SMALLER_long"][0],
               REF_NEAREST["PROPOSED_LEAD"][0], out["Comment_lead"][0], REF_NEAREST["PRED_PTPK"][0],
               np.round(REF_NEAREST["PRED_BASE_FREIGHT"][0]),
               REF_NEAREST["PTPK_CHANGEperKM"][0], REF_NEAREST["Lead_diff"][0],
               REF_NEAREST["PTPK_diff_from_Ref_city1"][0], ref_data_frame["COMMENT"][0]]]

    map_dataframe = pd.DataFrame(map_df,
                                 columns=["PLANT_CODE", "PLANT_NAME", "SOURCE_LAT", "SOURCE_LONG", "DESTINATION_NAME",
                                          "DESTINATION_LAT", "DESTINATION_LONG", "GOOGLE_DIST_PLANT_DEST",
                                          "REF_CITY_CODE1", "REF_CITY_CODE2", "REF_LAT1", "REF_LONG1", "REF_LAT2",
                                          "REF_LONG2", "NEAREST_GREATER_LAT", "NEAREST_GREATER_LONG",
                                          "NEAREST_SMALLER_LAT", "NEAREST_SMALLER_LONG", "PROPOSED_LEAD",
                                          "COMMENT_LEAD", "PRED_PTPK",
                                          "PRED_BASE_FREIGHT", "PTPK_CHANGEperKM", "Lead_diff",
                                          "PTPK_diff_from_Ref_city1", "Comment"])
    destination = address1  # CHANGE
    out_simi = [[destination, TRUCK_TYPE, taluka, DIRECT_STO]]

    out_simi = pd.DataFrame(out_simi, columns=["CITY_DESC", "TRUCK_TYPE", "TALUKA", "Direct_STO"])
    out_simi = pd.concat([out, out_simi], axis=1)

    out_simi['OD Pair'] = out_simi['PLANT'].apply(str) + "-" + out_simi['CITY_DESC']
    out_simi['CITY_CODE'] = out_simi['CITY_DESC']

    out_simi[['I2_TALUKA', 'I2_TALUKA_DESC']] = out_simi.TALUKA.str.split("-", 1, expand=True)

    out_simi.rename(
        columns={"PLANT": "DELVRY_PLANT", "New_destination_LAT": "Latitude", "New_destination_LONG": "Longitude"},
        inplace=True)

    if similarity == True:

        rc1 = feature_extraction(out_simi, waypoints)
        simi_result1 = simi_algorithm(simi_data, rc1, DIRECT_STO, map_dataframe, out, dispatchdata, taluka, PLANT)
        try:
            similarity_result = simi_result1[0]
            similarity_predicted_ptpk = np.round(simi_result1[1]["Predicted PTPK"][0], 2)
            map_dataframe["similarity_predicted_ptpk"] = similarity_predicted_ptpk
            return REFERENCE_DATAFRAME, NEAREST_DATAFRAME, map_dataframe, similarity_result, similarity_predicted_ptpk
        except:

            similarity_result = simi_result1[0]
            similarity_predicted_ptpk = "No suggested PTPK"
            map_dataframe["similarity_predicted_ptpk"] = similarity_predicted_ptpk

            return REFERENCE_DATAFRAME, NEAREST_DATAFRAME, map_dataframe, similarity_result, similarity_predicted_ptpk



    else:

        return REFERENCE_DATAFRAME, NEAREST_DATAFRAME, map_dataframe

#################################################################################################

'''  
function for one new destination

'''


def function1(PLANT, TALUKA, TRUCK_TYPE, DIRECT_STO, address1, similarity, PLANT_NAME, taluka, waypoints, Lead=np.nan):
    # print("Into function1: ")
    LAT = address1.split(',', 2)[0]
    LONG = address1.split(',', 2)[1]
    # print("Lat: ", LAT)
    # print("Lng: ", LONG)
    # print(LONG.isnumeric())
    check = address1.replace(".", "")
    check1 = check.replace(",", "")
    if check1.isdigit() == True:
        LAT = float(address1.split(',', 2)[0])
        LONG = float(address1.split(',', 2)[1])
        if Validate_coordinate(LAT, LONG) == True:
            # print("Output_function execution if isalpha ")
            latlng = (LAT, LONG)
            address1 = reverse_geocode(latlng, key)
            output = Output_function(PLANT, PLANT_NAME, TALUKA, TRUCK_TYPE, DIRECT_STO, address1, LAT, LONG, similarity,
                                     dispatchdata, hierarchydata, taluka=taluka, Lead=Lead, waypoints=waypoints)
        else:
            output = "Error"
    else:
        # print("Output_function NOT isnumeric")
        output = Output_function(PLANT, PLANT_NAME, TALUKA, TRUCK_TYPE, DIRECT_STO, address1, LAT, LONG, similarity,
                                 dispatchdata, hierarchydata, taluka=taluka, Lead=Lead, waypoints=waypoints)
    # print("total api count = ", count)
    return output, map_data_result

# result = function1(PLANT, TALUKA, TRUCK_TYPE, DIRECT_STO, address1, similarity)

# ref_dataframe = result[0]
# nearest_dataframe = result[1]
# map_dataframe = result[2]
# similarity_dataframe = result[3]
# similarity_pred_ptpk = result[4]
#
# print("similarity_pred_ptpk: ",similarity_pred_ptpk)
# ref_dataframe.to_csv("/media/shruti/HDD/shruti/fare/fare_ultratech/NewDestination/TestRunOutput/latLngTest_ref_dataframe.csv",header=True,index=False)
# nearest_dataframe.to_csv("/media/shruti/HDD/shruti/fare/fare_ultratech/NewDestination/TestRunOutput/latLngTest_nearest_dataframe.csv",header=True,index=False)
# map_dataframe.to_csv("/media/shruti/HDD/shruti/fare/fare_ultratech/NewDestination/TestRunOutput/latLngTest_map_dataframe.csv",header=True,index=False)
# similarity_dataframe.to_csv("/media/shruti/HDD/shruti/fare/fare_ultratech/NewDestination/TestRunOutput/latLngTest_similarity_dataframe.csv",header=True,index=False)
