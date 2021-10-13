SIMILARITY_DATA_MAPPER = {
    'Zone': 'zone',
    'PLANT': 'plant',
    'Type': 'type',
    'CITY_CODE': 'city_code',
    'CITY_DESC': 'city_desc',
    'Simi_Type': 'simi_type',
    'Simi_CITY_CODE': 'simi_city_code',
    'SIMI_CITY_NAME': 'simi_city_name',
    'TRUCK_TYPE': 'truck_type',
    'Direct_STO': 'direct_sto',
    'mean.route.timetaken.': 'mean_route_time_taken',
    'mean_ele': 'mean_ele',
    'sd_ele': 'sd_ele',
    'NH_Per_ref': 'nh_per_ref',
    'SH_Per_ref': 'sh_per_ref',
    'Other_Per_ref': 'other_per_ref',
    'Lead': 'lead',
    'PTPK': 'ptpk',
    'Plain_Per_ref': 'plain_per_ref',
    'Hilly_Per_ref': 'hilly_per_ref',
    'OnwardTravel': 'onward_travel',
    'ReturnTravel': 'return_travel',
    'IdleTimeCust': 'idle_time_cust',
    'Slab': 'slab',
    'cityno': 'cityno',
    'Simi_Matching_prob(SimiCoeff)': 'simi_coeff',
    'PTPK_Pred': 'ptpk_pred',
    'Path': 'path',
    'QUANTITY': 'quantity',
    'Batch': 'batch',
    'Source_Lat': 'source_lat',
    'Source_Long': 'source_long',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Pred_Base.Freight': 'pred_base_freight',
    'Impact': 'impact',
    'Base.Freight': 'base_freight',
    'TALUKA': 'taluka',
    'I2_TALUKA_DESC': 'i2_taluka_desc',
    'T_TYPE': 't_type',
    'FULL PLANT NAME': 'full_plant_name',
    'Simi_CITY': 'simi_city',
    'FULL CITY': 'full_city',
    'ROUTE_1': 'route_1',
    'ROUTE': 'route',
    'ROUTE_2': 'route_2',
    'PLANT_NAME': 'plant_name',
    'SIMI_ROUTE': 'simi_route',
    'Total_Restriction_time': 'total_restriction_time',
    'INTEGRATION_FLAG': 'integration_flag',
    'CLUSTER_FLAG': 'cluster_flag',
    'UNION_FLAG': 'union_flag',
    'depot_code': 'depot_code',
    'depot_desc': 'depot_desc',
    'district_code': 'district_code',
    'district_desc': 'district_desc'
}

LAST_MONTH_TILL_END_FILTER = """date(day_and_time_of_dispach) between date(date_trunc('month', CURRENT_DATE)-'1 month'::interval)
and date( date_trunc('month', CURRENT_DATE) - '1 day'::interval)"""

LAST_MONTH_FILTER = """date(day_and_time_of_dispach) between date(date_trunc('month', CURRENT_DATE)-'1 month'::interval) 
and date(CURRENT_DATE-'1 month'::interval)"""

CURRENT_MONTH_FILTER = """date(day_and_time_of_dispach) between date( date_trunc('month', CURRENT_DATE)) and date(CURRENT_DATE)"""

GREEN = "green"
RED = "red"

LIT_SOURCE = ('ADITYA', 'ALUPURAM', 'BELUR', 'HIRAKUD', 'MAHAN', 'MOUDA', 'RENUKOOT', 'TALOJA')
