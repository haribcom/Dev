import logging

from django.db.models import Q, Avg, F
from django.utils.datastructures import MultiValueDictKeyError

from chemical_analysis.controller import clean_similarity_data_new
from chemical_analysis.utils import list_of_similarity_field, add_location_graph, route, truncate
from ultratech_analysis.models import simi_data
from ultratech_core.models import Preferences

LOGGER = logging.getLogger(__name__)


# def clean_similarity_data(query):
#     """
#     This fn removes dec places of data as req
#     :param query:
#     :return:
#     """
#     for each_query in query:
#         each_query['quantity'] = round(each_query['quantity'])
#         each_query['meanElevation'] = round(each_query['meanElevation'])
#         each_query['standardElevation'] = round(each_query['standardElevation'])
#         each_query['avgLead'] = round(each_query['avgLead'])
#         each_query['simiCoeff'] = round(each_query['simiCoeff'], 2)
#         each_query['PTPK'] = round(each_query['PTPK'], 2)
#         each_query['avgIdleTimeCust'] = round(each_query['avgIdleTimeCust'], 2)
#         each_query['avgOnwardTravel'] = round(each_query['avgOnwardTravel'], 2)
#         each_query['hillyPer'] = round(each_query['hillyPer'], 2)
#         each_query['plainPer'] = round(each_query['plainPer'], 2)
#         each_query['nhPer'] = round(each_query['nhPer'], 2)
#         each_query['shPer'] = round(each_query['shPer'], 2)


# def clean_route_data(data):
#     for each_data in data:
#         each_data['Impact'] = round(each_data['Impact'])
#         each_data['Lead'] = round(each_data['Lead'])
#         each_data['PTPK'] = round(each_data['PTPK'], 2)
#         if each_data['PTPK_Pred']:
#             each_data['PTPK_Pred'] = round(each_data['PTPK_Pred'], 2)
#         each_data['QUANTITY'] = round(each_data['QUANTITY'])
#         each_data['simiCoeff'] = round(each_data['simiCoeff'], 2)


# def clean_route_data_ultratech(data):
#     """
#     Fn will clean the route data for ultratech
#     :param data:
#     :return:
#     """
#     for each_data in data:
#         each_data['impact'] = round(each_data['impact'])
#         each_data['lead'] = round(each_data['lead'])
#         each_data['PTPK'] = round(each_data['PTPK'], 2)
#         if each_data['PTPK_Pred']:
#             each_data['PTPK_Pred'] = round(each_data['PTPK_Pred'], 2)
#         each_data['quantity'] = round(each_data['quantity'])
#         each_data['simiCoeff'] = round(each_data['simiCoeff'], 2)


def drop_down():
    """
    This is the control fn for ultra tech drop down api
    :return:
    """
    query = simi_data.objects.all() \
        .values('plant', 'taluka', 'city_code', 'route', 'slab', 'truck_type', 't_type',
                'direct_sto').order_by('plant', 'taluka', 'city_code', 'truck_type')
    response = list_of_similarity_field(query, ultra_tech=True)
    return response


def plant_path_query(plant, path, taluka, city_code, truck_type):
    """
    This is the controller to get the data based on the path and plant selected.
    :param city_code:
    :param taluka:
    :param plant:
    :param path:
    :return:
    """
    try:
        path_selected = path
        plant_selected = plant
        round_off = list(Preferences.objects.filter(key="round").
                         values('value'))[0]['value'].split(',')
        round_off2 = list(Preferences.objects.filter(key="round2").
                          values('value'))[0]['value'].split(',')

        response = list()
        other_data = dict()
        # Adding data for dropdown
        dd_query = list_dict_dd(plant=plant, path=path,
                                city_code=city_code, truck_type=truck_type,
                                taluka=taluka)
        drop_down = dict()
        drop_down['dropDown'] = dd_query
        response.append(drop_down)

        data = simi_data.objects.filter(route=path_selected, plant=plant_selected,
                                        taluka=taluka, city_code=city_code, truck_type=truck_type).filter(
            ~Q(simi_coeff=1)). \
            annotate(simiCoeff=Avg("simi_coeff"),
                     meanElevation=F("mean_ele"), standardElevation=F("sd_ele"),
                     avgIdleTimeCust=Avg("idle_time_cust"), avgOnwardTravel=Avg("onward_travel"),
                     hillyPer=F("hilly_per"), plainPer=F("plain_per"),
                     nhPer=F("nh_per"), shPer=F("sh_per"), avgLead=Avg("lead"),
                     preditedPTPK=F("ptpk_pred"), PTPK=F('ptpk'), Type=F('type'),
                     Simi_Type=F("simi_type")).values(
            "Type", 'simiCoeff', "PTPK", "quantity", "meanElevation",
            "standardElevation", "avgLead", "avgIdleTimeCust", "avgOnwardTravel", "hillyPer",
            "plainPer", "nhPer", "shPer", "Simi_Type", "latitude",
            "longitude", "preditedPTPK").order_by('-simiCoeff')
        if data:
            # clean_similarity_data(data)
            clean_similarity_data_new(data, round_off, round_off2)
            other_data['otherData'] = add_location_graph(data)
            response.append(other_data)

            route_data = list(simi_data.objects.filter(route=path_selected, plant=plant_selected,
                                                       taluka=taluka, city_code=city_code, truck_type=truck_type)
                .filter(~Q(simi_coeff=1)) \
                .annotate(simiCoeff=Avg("simi_coeff"), PTPK=F("ptpk")
                          , PTPK_Pred=F("ptpk_pred")).values \
                ("simi_route", "impact", "quantity", "lead", "simiCoeff", "PTPK", "PTPK_Pred").order_by(
                '-impact'))
            # clean_route_data_ultratech(route_data)
            clean_similarity_data_new(route_data, round_off, round_off2)
            _route = dict()
            _route['routeData'] = route(route_data)

            auto_data = simi_data.objects.filter(route=path_selected, plant=plant_selected,
                                                 taluka=taluka, city_code=city_code, truck_type=truck_type) \
                .values('plant', 'taluka', 'route', 'slab', 'truck_type', 't_type', 'city_code',
                        'direct_sto').order_by('plant', 'taluka', 'city_code', 'truck_type')
            cleaed_auto_data = list_of_similarity_field(auto_data, ultra_tech=True)[0]

            ptpk_pred = simi_data.objects.filter(route=path_selected, plant=plant_selected,
                                                 taluka=taluka, city_code=city_code, truck_type=truck_type).filter(
                Q(simi_coeff=1)). \
                annotate(preditedPTPK=F("ptpk_pred")).values(
                "preditedPTPK")
            LOGGER.info("Ptpk Pred : {}".format(ptpk_pred))
            if ptpk_pred:
                _route["ptpkPred"] = truncate(ptpk_pred[0]["preditedPTPK"], 2)
            else:
                _route["ptpkPred"] = "N/A"
            response.append(_route)
            response.append(cleaed_auto_data)

            return response, 200
        else:
            LOGGER.info("Combination not possible. Path {} and plant {}".
                        format(path_selected, plant_selected))
            return {"message": "It is not possible to reach {} plant following {} path. "
                               "Please select other combination.".format(plant_selected, path_selected)}, 400
    except MultiValueDictKeyError as data_error:
        LOGGER.error("ERROR while receiving data from POST request %s", data_error,
                     exc_info=True)


def plant_dd(plant):
    """
    This is the fn that returns taluka, city code, truck type and path based on plant selected
    :param plant:
    :return:
    """
    query = simi_data.objects.filter(plant=plant).values('plant', 'taluka', 'city_code', 'truck_type', 'route',
                                                         'slab', 't_type', 'direct_sto') \
        .order_by('plant', 'taluka', 'city_code', 'truck_type')
    flag, dd_query = drop_down_filter(query)
    LOGGER.info("Drop down query: {}".format(query))
    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)
    if flag:
        return plant_path_query(plant=drop_down['dropDown'][0]['plant'][0],
                                taluka=drop_down['dropDown'][0]['taluka'][0],
                                city_code=drop_down['dropDown'][0]['cityCode'][0],
                                truck_type=drop_down['dropDown'][0]['truckType'][0],
                                path=drop_down['dropDown'][0]['pathSelected'][0])

    return response, 200


def plant_taluka_dd(plant, taluka):
    """
    This fn returns everythind for drop down based on the plant and taluka
    :param plant:
    :param taluka:
    :return:
    """
    query = simi_data.objects.filter(plant=plant, taluka=taluka).values('plant', 'taluka', 'city_code', 'truck_type',
                                                                        'route',
                                                                        'slab', 't_type', 'direct_sto'). \
        order_by('plant', 'taluka', 'city_code', 'truck_type')
    flag, dd_query = drop_down_filter(query)
    LOGGER.info("Drop down query: {}".format(query))

    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)
    if flag:
        return plant_path_query(plant=drop_down['dropDown'][0]['plant'][0],
                                taluka=drop_down['dropDown'][0]['taluka'][0],
                                city_code=drop_down['dropDown'][0]['cityCode'][0],
                                truck_type=drop_down['dropDown'][0]['truckType'][0],
                                path=drop_down['dropDown'][0]['pathSelected'][0])

    return response, 200

    # other_data = dict()
    #
    # data = simi_data.objects.filter(plant=plant, taluka=taluka).filter(
    #     ~Q(simi_coeff=1)). \
    #     annotate(simiCoeff=Avg("simi_coeff"),
    #              meanElevation=F("mean_ele"), standardElevation=F("sd_ele"),
    #              avgIdleTimeCust=Avg("idle_time_cust"), avgOnwardTravel=Avg("onward_travel"),
    #              hillyPer=F("hilly_per"), plainPer=F("plain_per"),
    #              nhPer=F("nh_per"), shPer=F("sh_per"), avgLead=Avg("lead"),
    #              preditedPTPK=F("ptpk_pred"), PTPK=F('ptpk'), Type=F('type'),
    #              Simi_Type=F("simi_type")).values(
    #     "Type", 'simiCoeff', "PTPK", "quantity", "meanElevation",
    #     "standardElevation", "avgLead", "avgIdleTimeCust", "avgOnwardTravel", "hillyPer",
    #     "plainPer", "nhPer", "shPer", "Simi_Type", "latitude",
    #     "longitude", "preditedPTPK").order_by('-simiCoeff')
    # if data:
    #     # clean_similarity_data(data)
    #     clean_similarity_data_new(data, round_off, round_off2)
    #     other_data['otherData'] = add_location_graph(data)
    #     response.append(other_data)
    #
    #     route_data = list(simi_data.objects.filter(plant=plant, taluka=taluka)
    #         .filter(~Q(simi_coeff=1)) \
    #         .annotate(simiCoeff=Avg("simi_coeff"), PTPK=F("ptpk")
    #                   , PTPK_Pred=F("ptpk_pred")).values \
    #         ("simi_route", "impact", "quantity", "lead", "simiCoeff", "PTPK", "PTPK_Pred").order_by(
    #         '-impact'))
    #     # clean_route_data_ultratech(route_data)
    #     clean_similarity_data_new(route_data, round_off, round_off2)
    #     _route = dict()
    #     _route['routeData'] = route(route_data)
    #     # response.append(_route)
    #
    #     # auto_data = simi_data.objects.filter(plant=plant, taluka=taluka) \
    #     #     .values('plant', 'taluka', 'route', 'slab', 'truck_type', 't_type', 'city_code',
    #     #             'direct_sto')
    #     # cleaed_auto_data = list_of_similarity_field(auto_data, ultra_tech=True)[0]
    #
    #     ptpk_pred = simi_data.objects.filter(plant=plant, taluka=taluka).filter(
    #         Q(simi_coeff=1)). \
    #         annotate(preditedPTPK=F("ptpk_pred")).values(
    #         "preditedPTPK")
    #     if ptpk_pred:
    #         _route["ptpkPred"] = truncate(ptpk_pred[0]["preditedPTPK"], 2)
    #     else:
    #         _route["ptpkPred"] = ""
    #     response.append(_route)
    #     return response


def plant_taluka_cc_dd(plant, taluka, city_code):
    """
    This fn gives all the drop down based on plant, taluka and city code selected
    :param plant:
    :param taluka:
    :param city_code:
    :return:
    """
    query = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code) \
        .values('plant', 'taluka', 'city_code', 'truck_type',
                'route', 'slab', 't_type', 'direct_sto'). \
        order_by('plant', 'taluka', 'city_code', 'truck_type')
    LOGGER.info("Drop down query: {}".format(query))
    # return drop_down_filter(query)
    # round_off = list(Preferences.objects.filter(key="round").
    #                  values('value'))[0]['value'].split(',')
    # round_off2 = list(Preferences.objects.filter(key="round2").
    #                   values('value'))[0]['value'].split(',')

    # response = list()

    flag, dd_query = drop_down_filter(query)

    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)
    if flag:
        return plant_path_query(plant=drop_down['dropDown'][0]['plant'][0],
                                taluka=drop_down['dropDown'][0]['taluka'][0],
                                city_code=drop_down['dropDown'][0]['cityCode'][0],
                                truck_type=drop_down['dropDown'][0]['truckType'][0],
                                path=drop_down['dropDown'][0]['pathSelected'][0])

    return response, 200
    # other_data = dict()
    #
    # data = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code).filter(
    #     ~Q(simi_coeff=1)). \
    #     annotate(simiCoeff=Avg("simi_coeff"),
    #              meanElevation=F("mean_ele"), standardElevation=F("sd_ele"),
    #              avgIdleTimeCust=Avg("idle_time_cust"), avgOnwardTravel=Avg("onward_travel"),
    #              hillyPer=F("hilly_per"), plainPer=F("plain_per"),
    #              nhPer=F("nh_per"), shPer=F("sh_per"), avgLead=Avg("lead"),
    #              preditedPTPK=F("ptpk_pred"), PTPK=F('ptpk'), Type=F('type'),
    #              Simi_Type=F("simi_type")).values(
    #     "Type", 'simiCoeff', "PTPK", "quantity", "meanElevation",
    #     "standardElevation", "avgLead", "avgIdleTimeCust", "avgOnwardTravel", "hillyPer",
    #     "plainPer", "nhPer", "shPer", "Simi_Type", "latitude",
    #     "longitude", "preditedPTPK").order_by('-simiCoeff')
    # if data:
    #     # clean_similarity_data(data)
    #     clean_similarity_data_new(data, round_off, round_off2)
    #     other_data['otherData'] = add_location_graph(data)
    #     response.append(other_data)
    #
    #     route_data = list(simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code)
    #         .filter(~Q(simi_coeff=1)) \
    #         .annotate(simiCoeff=Avg("simi_coeff"), PTPK=F("ptpk")
    #                   , PTPK_Pred=F("ptpk_pred")).values \
    #         ("simi_route", "impact", "quantity", "lead", "simiCoeff", "PTPK", "PTPK_Pred").order_by(
    #         '-impact'))
    #     # clean_route_data_ultratech(route_data)
    #     clean_similarity_data_new(route_data, round_off, round_off2)
    #     _route = dict()
    #     _route['routeData'] = route(route_data)
    #     # response.append(_route)
    #
    #     # auto_data = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code) \
    #     #     .values('plant', 'taluka', 'route', 'slab', 'truck_type', 't_type', 'city_code',
    #     #             'direct_sto')
    #     # cleaed_auto_data = list_of_similarity_field(auto_data, ultra_tech=True)[0]
    #
    #     ptpk_pred = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code).filter(
    #         Q(simi_coeff=1)). \
    #         annotate(preditedPTPK=F("ptpk_pred")).values(
    #         "preditedPTPK")
    #     if ptpk_pred:
    #         _route["ptpkPred"] = truncate(ptpk_pred[0]["preditedPTPK"], 2)
    #     else:
    #         _route["ptpkPred"] = ""
    #     response.append(_route)
    #     return response


def plant_taluka_cc_tt_dd(plant, taluka, city_code, truck_type):
    """

    :param plant:
    :param taluka:
    :param city_code:
    :param truck_type:
    :return:
    """
    query = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code, truck_type=truck_type) \
        .values('plant', 'taluka', 'city_code', 'truck_type',
                'route', 'slab', 't_type', 'direct_sto'). \
        order_by('plant', 'taluka', 'city_code', 'truck_type')
    LOGGER.info("Drop down query: {}".format(query))
    # return drop_down_filter(query)
    # round_off = list(Preferences.objects.filter(key="round").
    #                  values('value'))[0]['value'].split(',')
    # round_off2 = list(Preferences.objects.filter(key="round2").
    #                   values('value'))[0]['value'].split(',')

    # response = list()

    flag, dd_query = drop_down_filter(query)

    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)
    if flag:
        return plant_path_query(plant=drop_down['dropDown'][0]['plant'][0],
                                taluka=drop_down['dropDown'][0]['taluka'][0],
                                city_code=drop_down['dropDown'][0]['cityCode'][0],
                                truck_type=drop_down['dropDown'][0]['truckType'][0],
                                path=drop_down['dropDown'][0]['pathSelected'][0])

    return response, 200
    # other_data = dict()
    #
    # data = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code).filter(
    #     ~Q(simi_coeff=1)). \
    #     annotate(simiCoeff=Avg("simi_coeff"),
    #              meanElevation=F("mean_ele"), standardElevation=F("sd_ele"),
    #              avgIdleTimeCust=Avg("idle_time_cust"), avgOnwardTravel=Avg("onward_travel"),
    #              hillyPer=F("hilly_per"), plainPer=F("plain_per"),
    #              nhPer=F("nh_per"), shPer=F("sh_per"), avgLead=Avg("lead"),
    #              preditedPTPK=F("ptpk_pred"), PTPK=F('ptpk'), Type=F('type'),
    #              Simi_Type=F("simi_type")).values(
    #     "Type", 'simiCoeff', "PTPK", "quantity", "meanElevation",
    #     "standardElevation", "avgLead", "avgIdleTimeCust", "avgOnwardTravel", "hillyPer",
    #     "plainPer", "nhPer", "shPer", "Simi_Type", "latitude",
    #     "longitude", "preditedPTPK").order_by('-simiCoeff')
    # if data:
    #     # clean_similarity_data(data)
    #     clean_similarity_data_new(data, round_off, round_off2)
    #     other_data['otherData'] = add_location_graph(data)
    #     response.append(other_data)
    #
    #     route_data = list(simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code)
    #         .filter(~Q(simi_coeff=1)) \
    #         .annotate(simiCoeff=Avg("simi_coeff"), PTPK=F("ptpk")
    #                   , PTPK_Pred=F("ptpk_pred")).values \
    #         ("simi_route", "impact", "quantity", "lead", "simiCoeff", "PTPK", "PTPK_Pred").order_by(
    #         '-impact'))
    #     # clean_route_data_ultratech(route_data)
    #     clean_similarity_data_new(route_data, round_off, round_off2)
    #     _route = dict()
    #     _route['routeData'] = route(route_data)
    #
    #     # auto_data = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code) \
    #     #     .values('plant', 'taluka', 'route', 'slab', 'truck_type', 't_type', 'city_code',
    #     #             'direct_sto')
    #     # cleaed_auto_data = list_of_similarity_field(auto_data, ultra_tech=True)[0]
    #
    #     ptpk_pred = simi_data.objects.filter(plant=plant, taluka=taluka, city_code=city_code).filter(
    #         Q(simi_coeff=1)). \
    #         annotate(preditedPTPK=F("ptpk_pred")).values(
    #         "preditedPTPK")
    #     if ptpk_pred:
    #         _route["ptpkPred"] = truncate(ptpk_pred[0]["preditedPTPK"], 2)
    #     else:
    #         _route["ptpkPred"] = ""
    #     # response.append(cleaed_auto_data)
    #     response.append(_route)
    #     return response


def drop_down_filter(query):
    """
    This fn creates a drop down based on the plant selected
    :param query:
    :return:
    """
    response = list()
    each_response = dict()
    response.append(each_response)

    flag = True  # ideal case. need to call the display fn
    plant = set()
    taluka = set()
    path_selected = set()
    slab = set()
    truck_type = set()
    type = set()
    direct_sto = set()
    city_code = set()

    for each_relation in query:
        plant.add(each_relation.get('plant'))
        taluka.add(each_relation.get('taluka'))
        path_selected.add(each_relation.get('route'))
        slab.add(each_relation.get('slab'))
        truck_type.add(each_relation.get('truck_type'))
        direct_sto.add(each_relation.get('direct_sto'))
        type.add(each_relation.get('t_type'))
        city_code.add(each_relation.get('city_code'))

    each_response['plant'] = list(plant)
    each_response['taluka'] = list(taluka)
    each_response['pathSelected'] = list(path_selected)
    each_response['slab'] = list(slab)
    each_response['truckType'] = list(truck_type)
    each_response['type'] = list(type)
    each_response['directSTO'] = list(direct_sto)
    each_response['cityCode'] = list(city_code)
    if (len(plant) > 1) or (len(taluka) > 1) or (len(city_code) > 1) or (len(truck_type) > 1) or (
            len(path_selected) > 1):
        return False, response
    return True, response


def list_dict_dd(plant, taluka, city_code, truck_type, path):
    """
    This fn creates a list of dict for the drop down
    :param plant:
    :param taluka:
    :param city_code:
    :param truck_type:
    :param path:
    :return:
    """
    res = list()
    res_dict = dict()
    res_dict['plant'] = [plant]
    res_dict['taluka'] = [taluka]
    res_dict['pathSelected'] = [path]
    res_dict['truckType'] = [truck_type]
    res_dict['cityCode'] = [city_code]
    res.append(res_dict)
    return res
