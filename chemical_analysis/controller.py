import copy
import logging
from collections import OrderedDict

from django.db.models import Q, Avg, F
from django.utils.datastructures import MultiValueDictKeyError

from chemical_analysis.models import Chemical_Similarity_Data
from chemical_analysis.utils import list_of_similarity_field, add_location_graph, route, remove_simi_coeff_1, truncate, \
    capitalize, add_spacing
from chemical_core.models import Preferences

LOGGER = logging.getLogger(__name__)


#
# def clean_similarity_data(query):
#     for each_data in query:
#         each_data['nh_perc'] = round(each_data['nh_perc'], 2)
#         each_data['sh_perc'] = round(each_data['sh_perc'], 2)
#         each_data['hilly_perc'] = round(each_data['hilly_perc'], 2)
#         each_data['plain_perc'] = round(each_data['plain_perc'], 2)
#         each_data['ptpk'] = round(each_data['ptpk'], 2)
#         each_data['mean_ele'] = round(each_data['mean_ele'])
#         each_data['sd_ele'] = round(each_data['sd_ele'])
#         if each_data['ptpk_pred']:
#             each_data['ptpk_pred'] = round(each_data['ptpk_pred'])
#         each_data['avgQuantity'] = round(each_data['avgQuantity'])
#         each_data['avgTravleTime'] = round(each_data['avgTravleTime'], 2)
#         each_data['avgLead'] = round(each_data['avgLead'])
#         each_data['avg_simi_coeff'] = round(each_data['avg_simi_coeff'], 2)


def clean_similarity_data_new(query, round_off, round2):
    for each_data in query:
        for each_key in each_data:
            if each_key in round_off:
                if each_data[each_key]:
                    each_data[each_key] = truncate(each_data[each_key])
            if each_key in round2:
                if each_data[each_key]:
                    each_data[each_key] = truncate(each_data[each_key], 2)
        # each_data['nh_perc'] = round(each_data['nh_per'], 2)
        # each_data['sh_perc'] = round(each_data['sh_per'], 2)
        # each_data['hilly_perc'] = round(each_data['hilly_per'], 2)
        # each_data['plain_perc'] = round(each_data['plain_per'], 2)
        # each_data['ptpk'] = round(each_data['ptpk'], 2)
        # each_data['mean_ele'] = round(each_data['mean_ele'])
        # each_data['sd_ele'] = round(each_data['sd_ele'])
        # if each_data['ptpk_pred']:
        #     each_data['ptpk_pred'] = round(each_data['ptpk_pred'])
        # each_data['avgQuantity'] = round(each_data['avgQuantity'])
        # each_data['avgTravelTime'] = round(each_data['avgTravelTime'], 2)
        # each_data['avgLead'] = round(each_data['avgLead'])
        # each_data['avg_simi_coeff'] = round(each_data['avg_simi_coeff'], 2)


# def clean_route_data(query_list):
#     for each_query in query_list:
#         if each_query['impact']:
#             each_query['impact'] = truncate(each_query['impact'])
#         if each_query['lead']:
#             each_query['lead'] = truncate(each_query['lead'])
#         if each_query['simiCoeff']:
#             each_query['simiCoeff'] = truncate(each_query['simiCoeff'], 2)
#         if each_query['PTPK']:
#             each_query['PTPK'] = truncate(each_query['PTPK'])
#         if each_query['PTPK_Pred']:
#             each_query['PTPK_Pred'] = truncate(each_query['PTPK_Pred'], 2)
#         if each_query['quantity']:
#             each_query['quantity'] = truncate(each_query["quantity"])


def chemicals_drop_down():
    """
    Fn to return the drop down data in the chemicals dash board
    :return:
    """
    query = Chemical_Similarity_Data.objects.all() \
        .values('plant_name', 'taluka', 'route', 'slab', 'truck_type', 'type',
                'direct_sto', 'product', 'city_desc')
    flag, response = drop_down_filter(query)
    return response


def chemicals_display(plant, product, destination, path=None, toll=None):
    """
    Fn to return the data to display on dashboard based on the path, plant and product and toll
    :return:
    """
    try:
        round_off = list(Preferences.objects.filter(key="round").
                         values('value'))[0]['value'].split(',')
        round_2 = list(Preferences.objects.filter(key="round2").
                       values('value'))[0]['value'].split(',')

        LOGGER.info("Plant: {}".format(plant))
        LOGGER.info("Product: {}".format(product))
        LOGGER.info("Destination: {}".format(destination))
        path_selected = path
        plant_selected = plant
        product_selected = product
        LOGGER.info("Path selected: {}".format(path_selected))
        if toll:
            full_filter = Q(plant_name=plant, product=product, city_desc__iexact=destination, toll=toll)
        else:
            full_filter = Q(plant_name=plant, product=product, city_desc__iexact=destination)
        response = dict()

        dd_query = chem_list_dict_dd(plant=plant,
                                     product=product, destination=destination)

        response["dropDown"] = dd_query

        data = list(Chemical_Similarity_Data.objects.filter(full_filter) \
                    .filter(~Q(simi_coeff=1)).annotate(
            avgQuantity=Avg('quantity'), avgTravelTime=Avg('onward_travel'), avgLead=Avg('lead'),
            avg_simi_coeff=Avg('simi_coeff')). \
                    values('avgTravelTime', 'nh_per', 'sh_per', 'hilly_per', 'plain_per', 'avg_simi_coeff',
                           'ptpk', 'avgQuantity', 'mean_ele', 'sd_ele', 'avgLead', 'ptpk_pred',
                           'latitude', 'longitude', 'simi_type', 'simi_route',
                           'source_lat', 'source_long', 'plant_name', 'city_desc').order_by('-avg_simi_coeff'))[:5]
        current_data = list(Chemical_Similarity_Data.objects.filter(full_filter).filter(
            Q(simi_coeff=1)).annotate(
            avgQuantity=Avg('quantity'), avgTravelTime=Avg('onward_travel'), avgLead=Avg('lead')). \
                            values('avgTravelTime', 'nh_per', 'sh_per', 'hilly_per', 'plain_per',
                                   'ptpk', 'avgQuantity', 'mean_ele', 'sd_ele', 'avgLead', 'ptpk_pred',
                                   'latitude', 'longitude', 'simi_type', 'simi_route',
                                   'source_lat', 'source_long', 'plant_name', 'city_desc'))[:5]

        capitalize(data, "simi_route")
        capitalize(current_data, "simi_route")
        add_spacing(data, "simi_route")
        add_spacing(current_data, "simi_route")
        curr_ptpk = current_data[0]["ptpk"]
        del current_data[0]["ptpk"]

        simi_ptpk_data = list()
        simi_ptpk_data.append(current_data[0])

        # TODO: Add rem data
        simi_ptpk_data.extend(data)
        data.insert(0, current_data[0])
        capitalize(data, "city_desc")
        new_data = copy.deepcopy(data)
        del simi_ptpk_data[0]['simi_route']

        # TODO: Create separate for simi_coeff, simi_route and ptpk.

        if new_data:
            # data = remove_simi_coeff_1(data, "avg_simi_coeff")
            clean_similarity_data_new(new_data, round_off, round_2)
            clean_similarity_data_new(simi_ptpk_data, round_off, round_2)
            query_locatn = add_location_graph(new_data)
            response["otherData"] = add_location_graph(query_locatn, "source_location", "source_lat", "source_long")
            response["simiPTPK"] = simi_ptpk_data

            route_data = Chemical_Similarity_Data.objects.filter(product=product,
                                                                 plant_name=plant_selected,
                                                                 Path="Path").filter(~Q(impact=0)).annotate(
                simiCoeff=Avg("simi_coeff"), PTPK=F('ptpk'), PTPK_Pred=F('ptpk_pred'),
            ).values("route_1", "impact", "lead",
                     "simiCoeff", "PTPK",
                     "PTPK_Pred", "quantity").order_by('-impact')
            if toll:
                route_data = route_data.filter(toll=toll)
            route_data = list(route_data)
            query_route = list(Chemical_Similarity_Data.objects.filter(full_filter,
                                                                       Path="Path").
                               annotate(simiCoeff=Avg("simi_coeff"), PTPK=F('ptpk'), PTPK_Pred=F('ptpk_pred'),
                                        ).values("route_1", "impact", "lead",
                                                 "simiCoeff", "PTPK",
                                                 "PTPK_Pred", "quantity")
                               .order_by('-impact'))
            LOGGER.info("Route data originating from curr plant : {}".format(route_data))
            LOGGER.info("Current route selected: {}".format(query_route))
            # Removed duplicate path from the route
            if query_route[0] in route_data:
                route_data.remove(query_route[0])
                route_data.insert(0, query_route[0])

            # clean_route_data(route_data)
            clean_similarity_data_new(route_data, round_off, round_2)
            # route_data = remove_simi_coeff_1(route_data, "simiCoeff")
            response['routeData'] = route(route_data)

            auto_data = Chemical_Similarity_Data.objects.filter(full_filter) \
                .values('plant_name', 'taluka', 'route', 'slab', 'truck_type', 'type',
                        'direct_sto', 'product')
            # response.append(list_of_similarity_field(auto_data, chemicals=True)[0])

            cleaed_auto_data = list_of_similarity_field(auto_data, chemicals=True)[0]

            # TODO: Removes current query (check)

            if current_data:
                response["source"] = plant
                response["destination"] = destination
                response["ptpkPred"] = truncate(current_data[0]["ptpk_pred"], 2)
                response["currPtpk"] = truncate(curr_ptpk, 2)
                response["currQuantity"] = truncate(current_data[0]["avgQuantity"], 0)
            else:
                response["ptpkPred"] = ""
            response["simiDropDown"] = cleaed_auto_data
            return response
        else:
            LOGGER.info("Combination not possible. Path {} and plant {}".
                        format(path_selected, plant_selected))
            return

    except MultiValueDictKeyError as data_error:
        LOGGER.error("ERROR while receiving data from POST request for chemicals %s", data_error,
                     exc_info=True)


def product_dd(product):
    """
    Fn to get the drop down based on the product
    :param product:
    :return:
    """
    query = Chemical_Similarity_Data.objects.filter(product=product) \
        .values('plant_name', 'city_desc', 'taluka', 'route', 'slab', 'truck_type', 'type',
                'direct_sto', 'product')
    flag, dd_query = drop_down_filter(query)
    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)
    # other_data = dict()

    if flag:
        return chemicals_display(
            product=drop_down['dropDown'][0]['product'][0],
            destination=drop_down['dropDown'][0]['city_desc'][0],
            plant=drop_down['dropDown'][0]['plant'][0] if type(drop_down['dropDown'][0]['plant'][0]) == list else drop_down['dropDown'][0]['plant'])
    return response


def product_plant_dd(product, plant):
    """
    Fn to get the drop down based on product and plant
    :param product:
    :param plant:
    :return:
    """
    # round_off = list(Preferences.objects.filter(key="round").
    #                  values('value'))[0]['value'].split(',')
    # round_2 = list(Preferences.objects.filter(key="round2").
    #                values('value'))[0]['value'].split(',')
    query = Chemical_Similarity_Data.objects.filter(product=product, plant_name=plant) \
        .values('plant_name', 'city_desc', 'taluka', 'route', 'slab', 'truck_type', 'type',
                'direct_sto', 'product')
    # return drop_down_filter(query)
    flag, dd_query = drop_down_filter(query)
    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)
    if flag:
        return chemicals_display(
            product=drop_down['dropDown'][0]['product'][0],
            destination=drop_down['dropDown'][0]['city_desc'][0],
            plant=plant)
    return drop_down

    # other_data = dict()
    #
    # data = Chemical_Similarity_Data.objects.filter(product=product, plant=plant).filter(~Q(simi_coeff=1)).annotate(
    #     avgQuantity=Avg('quantity'), avgTravelTime=Avg('onward_travel'), avgLead=Avg('lead'),
    #     avg_simi_coeff=Avg('simi_coeff')). \
    #     values('avgTravelTime', 'nh_per', 'sh_per', 'hilly_per', 'plain_per', 'avg_simi_coeff',
    #            'ptpk', 'avgQuantity', 'mean_ele', 'sd_ele', 'avgLead', 'ptpk_pred',
    #            'latitude', 'longitude', 'simi_type').order_by('-avg_simi_coeff')
    # if data:
    #     data = remove_simi_coeff_1(data, "avg_simi_coeff")
    #     clean_similarity_data_new(data, round_off, round_2)
    #     other_data['otherData'] = add_location_graph(data)
    #     response.append(other_data)
    #     route_data = list(Chemical_Similarity_Data.objects.filter(product=product, plant=plant)
    #                       .filter(~Q(simi_coeff=1)).
    #                       annotate(simiCoeff=Avg("simi_coeff"), PTPK=F('ptpk'), PTPK_Pred=F('ptpk_pred'),
    #                                ).values("route", "impact", "lead",
    #                                         "simiCoeff", "PTPK",
    #                                         "PTPK_Pred", "quantity")
    #                       .order_by('-impact'))
    #     # clean_route_data(route_data)
    #     clean_similarity_data_new(route_data, round_off, round_2)
    #     _route = dict()
    #     route_data = remove_simi_coeff_1(route_data, "simiCoeff")
    #     _route['routeData'] = route(route_data)
    #     # response.append(_route)
    #     # auto_data = Chemical_Similarity_Data.objects.filter(product=product, plant=plant) \
    #     #     .values('plant', 'taluka', 'route', 'slab', 'truck_type', 'type',
    #     #             'direct_sto', 'product')
    #     # # response.append(list_of_similarity_field(auto_data, chemicals=True)[0])
    #     #
    #     # cleaed_auto_data = list_of_similarity_field(auto_data, chemicals=True)[0]
    #
    #     ptpk_pred = Chemical_Similarity_Data.objects.filter(product=product, plant=plant).filter(
    #         Q(simi_coeff=1)). \
    #         annotate(preditedPTPK=F("ptpk_pred")).values(
    #         "preditedPTPK")
    #     if ptpk_pred:
    #         _route["ptpkPred"] = truncate(ptpk_pred[0]["preditedPTPK"], 2)
    #     else:
    #         _route["ptpkPred"] = ""
    #     response.append(_route)
    #     return response
    #
    # return drop_down_filter(query)


def product_plant_dest_dd(product, plant, destination, toll):
    # round_off = list(Preferences.objects.filter(key="round").
    #                  values('value'))[0]['value'].split(',')
    # round_2 = list(Preferences.objects.filter(key="round2").
    #                values('value'))[0]['value'].split(',')
    query = Chemical_Similarity_Data.objects.filter(product=product, plant_name=plant, city_desc__iexact=destination,
                                                    toll=toll) \
        .values('plant_name', 'city_desc', 'taluka', 'route', 'slab', 'truck_type', 'type',
                'direct_sto', 'product')
    # return drop_down_filter(query)
    flag, dd_query = drop_down_filter(query)
    response = list()
    drop_down = dict()
    drop_down['dropDown'] = dd_query
    response.append(drop_down)

    if flag:
        if drop_down['dropDown'][0]['product']:
            return chemicals_display(
                product=drop_down['dropDown'][0]['product'][0],
                destination=drop_down['dropDown'][0]['city_desc'][0],
                plant=plant,
                toll=toll)
        else:
            # Selection not possible
            return 400
    return response

    # other_data = dict()
    #
    # data = Chemical_Similarity_Data.objects.filter(product=product, plant=plant, city_desc=destination). \
    #     filter(~Q(simi_coeff=1)).annotate(
    #     avgQuantity=Avg('quantity'), avgTravelTime=Avg('onward_travel'), avgLead=Avg('lead'),
    #     avg_simi_coeff=Avg('simi_coeff')). \
    #     values('avgTravelTime', 'nh_per', 'sh_per', 'hilly_per', 'plain_per', 'avg_simi_coeff',
    #            'ptpk', 'avgQuantity', 'mean_ele', 'sd_ele', 'avgLead', 'ptpk_pred',
    #            'latitude', 'longitude', 'simi_type').order_by('-avg_simi_coeff')
    # if data:
    #     data = remove_simi_coeff_1(data, "avg_simi_coeff")
    #     clean_similarity_data_new(data, round_off, round_2)
    #     other_data['otherData'] = add_location_graph(data)
    #     response.append(other_data)
    #     route_data = list(Chemical_Similarity_Data.objects.filter(product=product, plant=plant, city_desc=destination)
    #                       .filter(~Q(simi_coeff=1)).
    #                       annotate(simiCoeff=Avg("simi_coeff"), PTPK=F('ptpk'), PTPK_Pred=F('ptpk_pred'),
    #                                ).values("route", "impact", "lead",
    #                                         "simiCoeff", "PTPK",
    #                                         "PTPK_Pred", "quantity")
    #                       .order_by('-impact'))
    #     # clean_route_data(route_data)
    #     clean_similarity_data_new(route_data, round_off, round_2)
    #     _route = dict()
    #     route_data = remove_simi_coeff_1(route_data, "simiCoeff")
    #     _route['routeData'] = route(route_data)
    #     # response.append(_route)
    #     # auto_data = Chemical_Similarity_Data.objects.filter(product=product, plant=plant, city_desc=destination) \
    #     #     .values('plant', 'taluka', 'route', 'slab', 'truck_type', 'type',
    #     #             'direct_sto', 'product')
    #     # # response.append(list_of_similarity_field(auto_data, chemicals=True)[0])
    #     #
    #     # cleaed_auto_data = list_of_similarity_field(auto_data, chemicals=True)[0]
    #
    #     ptpk_pred = Chemical_Similarity_Data.objects.filter(product=product, plant=plant, city_desc=destination).filter(
    #         Q(simi_coeff=1)). \
    #         annotate(preditedPTPK=F("ptpk_pred")).values(
    #         "preditedPTPK")
    #     if ptpk_pred:
    #         _route["ptpkPred"] = truncate(ptpk_pred[0]["preditedPTPK"], 2)
    #     else:
    #         _route["ptpkPred"] = ""
    #     response.append(_route)
    #     return response
    #
    # return drop_down_filter(query)


def drop_down_filter(query):
    """
    Fn to adjust drop down for chemicals
    :param query:
    :return:
    """
    response = list()
    each_response = OrderedDict()
    response.append(each_response)
    plant = set()
    taluka = set()
    path_selected = set()
    slab = set()
    truck_type = set()
    type = set()
    direct_sto = set()
    product = set()
    city_desc = set()

    for each_relation in query:
        plant.add(each_relation.get('plant_name'))
        taluka.add(each_relation.get('taluka'))
        path_selected.add(each_relation.get('route'))
        slab.add(each_relation.get('slab'))
        truck_type.add(each_relation.get('truck_type'))
        direct_sto.add(each_relation.get('direct_sto'))
        city_desc.add(each_relation.get('city_desc').capitalize())
        product.add(each_relation.get('product'))
        type.add(each_relation.get('type'))

    each_response['plant'] = list(plant)
    sorted_plant = sorted(each_response['plant'])
    each_response['plant'] = sorted_plant if len(sorted_plant) > 1 else sorted_plant[0]

    each_response['taluka'] = list(taluka)
    each_response['pathSelected'] = list(path_selected)
    each_response['slab'] = list(slab)
    each_response['truckType'] = list(truck_type)
    each_response['type'] = list(type)
    each_response['directSTO'] = list(direct_sto)

    each_response['product'] = list(product)
    sorted_product = sorted(each_response['product'])
    each_response['product'] = sorted_product

    each_response['city_desc'] = list(city_desc)
    sorted_destination = sorted(each_response['city_desc'])
    each_response['city_desc'] = sorted_destination

    if (len(plant) > 1) or (len(product) > 1) or (len(city_desc) > 1):
        return False, response
    return True, response


def chem_list_dict_dd(plant, product, destination, toll=None):
    """
    create dict of list
    :param toll:
    :param plant:
    :param product:
    :param destination:
    :return:
    """
    res = list()
    res_dict = dict()
    res_dict['plant'] = plant
    res_dict['city_desc'] = [destination]
    res_dict['product'] = [product]
    res_dict['toll'] = [toll]
    res.append(res_dict)
    return res
