import datetime
import re
from concurrent.futures._base import wait

from concurrent.futures.thread import ThreadPoolExecutor
import logging
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.utils import access_permissions, truncate, round_off
from dateutil.relativedelta import relativedelta
from hindalco import queries
from hindalco.constants import LIT_SOURCE, CURRENT_MONTH_FILTER, LAST_MONTH_FILTER, RED, GREEN, IN_PROGRESS, \
    AGE_FILTERS, AGE_FILTERS_ORDER, AGE_FILTERS_L3, IN_SUFFICIENT_DATA, DELAYED_CATEGORY, NON_DELAYED_CATEGORY, \
    DAYS_TO_DELIVER_FILTER, DAILY_DISTANCE_FILTER
from hindalco.utils import get_lit_connection_pool, get_month_no_from_name, format_offset
from utils import populate_xlxs_from_data, populate_xlxs_from_dict_data

LOGGER = logging.getLogger('django')


class LITView(viewsets.ViewSet):
    # permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.executor_pool = ThreadPoolExecutor(max_workers=10)
        self.connection_pool = get_lit_connection_pool()

    @access_permissions(('HIL', 'admin', 'Admin'))
    @action(detail=False, methods=['GET'], url_path='level1')
    def level1_dashboard(self, request, *args, **kwargs):
        try:
            response = dict()
            filters = {}
            for k, v in request.GET.items():
                if k and v and v != '' and len(v) > 0:
                    filters[k] = ",".join(["'{}'".format(each_value) for each_value in v.split(',')])
            months_input = None
            if not filters.get('source'):
                filters['source'] = ",".join(["'{}'".format(default_source) for default_source in LIT_SOURCE])
            if filters.get('month'):
                months_input = filters.get('month')
                filters.pop('month')
            filters = ["{} in ({})".format(k, v) for k, v in filters.items()]
            if months_input:
                filters.append(self.generate_date_filter_query(months=months_input))

            till_date, mtd_date = self.get_filter_date_min_max(months_input)
            response['till_date'] = till_date
            response['mtd_date'] = mtd_date
            async_db_calls = []
            data_name = []

            sql = queries.total_trips_graph.format(where="where " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "total_trips_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "total_trips_graph"))
            data_name.append("total_trips_graph")

            sql = queries.valid_trips_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "valid_trips_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "valid_trips_graph"))
            data_name.append("valid_trips_graph")

            sql = queries.open_trips_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "open_trips_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "open_trips_graph"))
            data_name.append('open_trips_graph')

            sql = queries.closed_trips_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "closed_trips_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "closed_trips_graph"))
            data_name.append("closed_trips_graph")

            sql = queries.geofence_closures_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "geofence_closures_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "geofence_closures_graph"))
            data_name.append('geofence_closures_graph')

            sql = queries.forceful_closures_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "forceful_closures_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "forceful_closures_graph"))
            data_name.append('forceful_closures_graph')

            sql = queries.delay_trips_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "delay_trips_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "delay_trips_graph"))
            data_name.append('delay_trips_graph')

            sql = queries.avg_daily_distance.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "avg_daily_distance")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "avg_daily_distance"))
            data_name.append('avg_daily_distance')

            sql = queries.avg_days_deliver_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "avg_days_deliver_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "avg_days_deliver_graph"))
            data_name.append('avg_days_deliver_graph')

            sql = queries.carbon_emission_graph.format(where=" and " + " and ".join(filters) if filters else '')
            # colnames, result = self.get_data_db(con, sql, cur, "carbon_emission_graph")
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "carbon_emission_graph"))
            data_name.append('carbon_emission_graph')

            _, pending = wait(async_db_calls)

            for itr in range(0, len(data_name)):
                try:
                    name = data_name[itr]
                    colnames, result = async_db_calls[itr].result()

                    if name == "avg_days_deliver_graph" or name == "avg_daily_distance":
                        response[name] = {'graph': self.format_graph(result)}
                        month_size = len(response[name]['graph'])
                        response[name]['total'] = self.divide(sum([i['trip_count'] for i in response[name]['graph']]),
                                                              month_size)
                    elif name in ("open_trips_graph", "closed_trips_graph"):
                        response[name] = {'graph': self.format_graph(result, response['valid_trips_graph']['graph'])}
                        response[name]['total'] = sum([i['trip_count'] for i in response[name]['graph']])
                    elif name in ("geofence_closures_graph", "forceful_closures_graph", "delay_trips_graph"):
                        response[name] = {'graph': self.format_graph(result, response['closed_trips_graph']['graph'])}
                        response[name]['total'] = sum([i['trip_count'] for i in response[name]['graph']])
                    else:
                        response[name] = {'graph': self.format_graph(result)}
                        response[name]['total'] = sum([i['trip_count'] for i in response[name]['graph']])
                except TypeError:
                    LOGGER.info("error while reading {}".format(name))

            async_db_calls = []
            sql = queries.avg_total_daily_distance.format(where=" and " + " and ".join(filters) if filters else '')
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "avg_total_daily_distance"))
            sql = queries.avg_total_days_deliver.format(where=" and " + " and ".join(filters) if filters else '')
            async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "avg_total_days_deliver"))

            _, pending = wait(async_db_calls)
            colnames, result = async_db_calls[0].result()
            response["avg_daily_distance"]["total"] = result[0][0]
            colnames, result = async_db_calls[1].result()
            response['avg_days_deliver_graph']["total"] = result[0][0]

            response['total_trips_graph']['qty'] = "-"
            response['valid_trips_graph']['qty'] = LITView.get_quantity(response['valid_trips_graph']['total'],
                                                                        response['total_trips_graph']['total'])
            response['open_trips_graph']['qty'] = LITView.get_quantity(response['open_trips_graph']['total'],
                                                                       response['valid_trips_graph']['total'])
            response['closed_trips_graph']['qty'] = LITView.get_quantity(response['closed_trips_graph']['total'],
                                                                         response['valid_trips_graph']['total'])
            response['geofence_closures_graph']['qty'] = LITView.get_quantity(
                response['geofence_closures_graph']['total'],
                response['closed_trips_graph']['total'])
            response['forceful_closures_graph']['qty'] = LITView.get_quantity(
                response['forceful_closures_graph']['total'],
                response['closed_trips_graph']['total'])
            response['delay_trips_graph']['qty'] = LITView.get_quantity(response['delay_trips_graph']['total'],
                                                                        response['closed_trips_graph']['total'])
            response['avg_daily_distance']['qty'] = truncate(response['avg_daily_distance']['total'], 2)
            response['avg_days_deliver_graph']['qty'] = truncate(response['avg_days_deliver_graph']['total'], 2)
            response['carbon_emission_graph']['qty'] = response['carbon_emission_graph']['total']

            if not months_input:
                cur_month_filter = filters.copy()
                last_month_filter = filters.copy()
                cur_month_filter.append(CURRENT_MONTH_FILTER)
                last_month_filter.append(LAST_MONTH_FILTER)

                async_db_calls = []
                data_name = []

                sql = queries.total_trips_count_curr_month.format(
                    where=" and ".join(cur_month_filter) if cur_month_filter else '')
                # colnames, total_trip_this_month = self.get_data_db(con, sql, cur, "total_trips_count_curr_month")
                async_db_calls.append(self.executor_pool.submit(self.get_data_db, sql, "total_trips_count_curr_month"))
                data_name.append("total_trips_graph")
                sql = queries.total_trips_count_last_month.format(
                    where=" and ".join(last_month_filter) if last_month_filter else '')
                # colnames, total_trip_last_month = self.get_data_db(con, sql, cur, "total_trips_count_curr_month")
                async_db_calls.append(
                    self.executor_pool.submit(self.get_data_db, sql, "total_trips_count_last_month"))
                data_name.append("total_trips_graph")

                sql = queries.valid_trips_count_this_month.format(
                    where=" and ".join(cur_month_filter) if cur_month_filter else '')
                # colnames, total_valid_trip_this_month = self.get_data_db(con,sql, cur, "total_trips_count_curr_month")
                async_db_calls.append(
                    self.executor_pool.submit(self.get_data_db, sql, "valid_trips_count_this_month"))
                data_name.append("valid_trips_graph")
                sql = queries.valid_trips_count_last_month.format(where=" and ".join(last_month_filter)
                if last_month_filter else '')
                # colnames, total_valid_trip_last_month = self.get_data_db(con,sql, cur, "valid_trips_count_last_month")
                async_db_calls.append(
                    self.executor_pool.submit(self.get_data_db, sql, "valid_trips_count_last_month"))
                data_name.append("valid_trips_graph")

                # sql = queries.avg_daily_distance_count_this_month.format(where=" and ".join(cur_month_filter)
                # if cur_month_filter else '')
                # colnames, avg_daily_distance_count_this_month = self.get_data_db(con, sql, cur,
                #                                                                  "avg_daily_distance_count_this_month")
                # async_db_calls.append(
                #     self.executor_pool.submit(self.get_data_db, sql, "avg_daily_distance_count_this_month"))
                # data_name.append("avg_daily_distance")
                # sql = queries.avg_daily_distance_count_last_month.format(where=" and ".join(last_month_filter)
                # if last_month_filter else '')
                # colnames, avg_daily_distance_count_last_month = self.get_data_db(con, sql, cur,
                #                                                                  "avg_daily_distance_count_last_month")
                # async_db_calls.append(
                #     self.executor_pool.submit(self.get_data_db, sql, "avg_daily_distance_count_last_month"))
                # data_name.append("avg_daily_distance")

                # sql = queries.avg_days_deliver_count_this_month.format(where=" and ".join(cur_month_filter)
                # if cur_month_filter else '')
                # colnames, avg_days_deliver_count_this_month = self.get_data_db(con, sql, cur,
                #                                                                "avg_days_deliver_count_this_month")
                # async_db_calls.append(
                #     self.executor_pool.submit(self.get_data_db, sql, "avg_days_deliver_count_this_month"))
                # data_name.append("avg_days_deliver_graph")
                # sql = queries.avg_days_deliver_count_last_month.format(where=" and ".join(last_month_filter)
                # if last_month_filter else '')
                # colnames, avg_days_deliver_count_last_month = self.get_data_db(con, sql, cur,
                #                                                                "avg_days_deliver_count_last_month")
                # async_db_calls.append(
                #     self.executor_pool.submit(self.get_data_db, sql, "avg_days_deliver_count_last_month"))
                # data_name.append("avg_days_deliver_graph")

                sql = queries.carbon_emission_count_this_month.format(where=" and ".join(cur_month_filter)
                if cur_month_filter else '')
                # colnames, carbon_emission_count_this_month = self.get_data_db(con, sql, cur,
                #                                                               "carbon_emission_count_this_month")
                async_db_calls.append(
                    self.executor_pool.submit(self.get_data_db, sql, "carbon_emission_count_this_month"))
                data_name.append("carbon_emission_graph")
                sql = queries.carbon_emission_count_last_month.format(where=" and ".join(last_month_filter)
                if last_month_filter else '')
                # colnames, carbon_emission_count_last_month = self.get_data_db(con, sql, cur,
                #                                                               "carbon_emission_count_last_month")
                async_db_calls.append(
                    self.executor_pool.submit(self.get_data_db, sql, "carbon_emission_count_last_month"))
                data_name.append("carbon_emission_graph")

                _, pending = wait(async_db_calls)
                db_calls = len(data_name)
                i = 0
                while i < db_calls:
                    try:
                        name = data_name[i]
                        colnames_this, result_this = async_db_calls[i].result()
                        colnames_last, result_last = async_db_calls[i + 1].result()
                        response[name]['percent'] = LITView.cal_percentage(result_this, result_last)
                        if name in ("carbon_emission_graph", "avg_days_deliver_graph", "delay_trips_graph"):
                            response[name]['color'] = RED if response[name]['percent'] > 0 else GREEN
                        else:
                            response[name]['color'] = GREEN if response[name]['percent'] > 0 else RED
                    except TypeError:
                        LOGGER.info("error while reading {}".format(name))
                    finally:
                        i = i + 2

                percent_based_graph = ["open_trips_graph", "closed_trips_graph", "geofence_closures_graph",
                                       "forceful_closures_graph", "delay_trips_graph"]
                for graph_name in percent_based_graph:
                    graph_data = response[graph_name]['graph']
                    # graph_data.sort(key=self.month_year_comparator_graph)
                    graph_size = len(graph_data)
                    if graph_size >= 2:
                        last_month, this_month = graph_data[graph_size - 2]['percent'], graph_data[graph_size - 1][
                            'percent']
                    else:
                        last_month = 0
                        if graph_size:
                            this_month = graph_data[graph_size - 1]['percent']
                        else:
                            this_month = 0
                    response[graph_name]["percent"] = this_month - last_month
                    if graph_name in ("forceful_closures_graph", "open_trips_graph", "delay_trips_graph"):
                        response[graph_name]['color'] = RED if response[graph_name]['percent'] > 0 else GREEN
                    else:
                        response[graph_name]['color'] = GREEN if response[graph_name]['percent'] > 0 else RED

                percent_based_graph_without_divider = ["avg_daily_distance", "avg_days_deliver_graph"]
                for graph_name in percent_based_graph_without_divider:
                    graph_data = response[graph_name]['graph']
                    graph_size = len(graph_data)
                    if graph_size >= 2:
                        last_month, this_month = graph_data[graph_size - 2]['trip_count'], graph_data[graph_size - 1][
                            'trip_count']
                    else:
                        last_month = 0
                        if graph_size:
                            this_month = graph_data[graph_size - 1]['trip_count']
                        else:
                            this_month = 0
                    response[graph_name]["percent"] = truncate(((this_month - last_month) / last_month) * 100, 2)
                    if graph_name == "avg_daily_distance":
                        response[graph_name]['color'] = GREEN if response[graph_name]['percent'] > 0 else RED
                    else:
                        response[graph_name]['color'] = RED if response[graph_name]['percent'] > 0 else GREEN


            async_db_calls = []
            data_name = []
            destination_filter_sql = queries.destination_filter
            # colnames, result = self.get_data_db(con, destination_filter_sql, cur, "destination_filter")
            async_db_calls.append(
                self.executor_pool.submit(self.get_data_db, destination_filter_sql, "destination_filter"))
            data_name.append("destination")

            month_date_filter_sql = queries.date_filter
            # colnames, result = self.get_data_db(con, month_date_filter_sql, cur, "date_filter")
            async_db_calls.append(
                self.executor_pool.submit(self.get_data_db, month_date_filter_sql, "date_filter"))
            data_name.append("date_filter")

            min_max_record_date_query = queries.max_min_date
            # colnames, result = self.get_data_db(con, min_max_record_date_query, cur, "max_min_date")
            async_db_calls.append(
                self.executor_pool.submit(self.get_data_db, min_max_record_date_query, "max_min_date"))
            data_name.append("max_min_date")

            _, pending = wait(async_db_calls)
            response["filter"] = dict()
            for itr in range(0, len(data_name)):
                name = data_name[itr]
                colnames, result = async_db_calls[itr].result()
                if name == "date_filter":
                    dates = [" ".join(each_destination[0].split()) for each_destination in result]
                    dates.sort(key=self.month_year_comparator)
                    response["filter"]["month"] = dates
                elif name == "max_min_date":
                    response["max_date"] = result[0][0]
                    response["min_date"] = result[0][1]
                else:
                    response["filter"][name] = [each_destination for each_destination in result]
            response["filter"]["source"] = LIT_SOURCE

        except Exception:
            LOGGER.exception("exception in LIT view")

        return Response(data=response)

    def get_data_db(self, query, query_name=None):
        try:
            LOGGER.info("=" * 25)
            LOGGER.info("{} sql start executing".format(query_name))
            LOGGER.info(query)
            con = self.connection_pool.getconn()
            cur = con.cursor()
            cur.execute(query)
            colnames = [desc[0] for desc in cur.description]
            result = cur.fetchall()
            LOGGER.info("{} sql completed".format(query_name))
            LOGGER.info("=" * 25)
            return colnames, result
        except Exception as ex:
            LOGGER.info("{} sql gives error".format(query_name))
            LOGGER.info(query)
            LOGGER.exception("exception while executing sql = {sql}".format(sql=query))
        finally:
            cur.close()
            self.connection_pool.putconn(con)

    @staticmethod
    def cal_percentage(this_month, last_month):
        try:
            this_month = this_month[0][0]
            last_month = last_month[0][0]
            return truncate(((this_month - last_month) / last_month) * 100, 2)
        except ZeroDivisionError:
            return 0
        except Exception:
            return 0

    @staticmethod
    def get_quantity(numerator, denominator, round_off_digit=2):
        try:
            return truncate((numerator / denominator) * 100, round_off_digit)
        except ZeroDivisionError:
            return 0
        except Exception:
            return 0

    def format_graph(self, result, divider=None):
        if divider:
            graph_data = []
            divider = {i['month']: i for i in divider}
            for each_month_data in result:
                agg_data = dict()
                agg_data['month'] = ", ".join(each_month_data[0].split())
                agg_data['compared_trip_count'] = divider[agg_data['month']]['trip_count']
                agg_data['trip_count'] = each_month_data[1]
                agg_data['percent'] = LITView.get_quantity(agg_data['trip_count'], agg_data['compared_trip_count'], 2)
                graph_data.append(agg_data)
            graph_data.sort(key=self.month_year_comparator_graph)
            return graph_data
        else:
            graph_data = [{'month': ", ".join(each_data[0].split()), 'trip_count': round_off(each_data[1], 2)} for
                          each_data
                          in
                          result]
            graph_data.sort(key=self.month_year_comparator_graph)
            return graph_data

    def generate_date_filter_query(self, months, relation=""):
        # dates = self.get_start_end_date_month(months)
        # template = "(day_and_time_of_dispach between '{start_date}' and '{end_date}')"
        # date_filters = " OR ".join([template.format(start_date=date[0], end_date=date[1]) for date in dates])

        new_template = "{relation}month={month}"
        months = months.split(',')
        date_filters = " OR ".join([new_template.format(relation=relation, month=month.strip()) for month in months])
        date_filters = "( " + date_filters + ") "
        return date_filters

    def get_start_end_date_month(self, months):
        import calendar
        month_year = months.split(',')
        start_end_date = []
        for each_month_year in month_year:
            year = re.search("[0-9]+", each_month_year).group()
            month = re.search("[a-zA-z]+", each_month_year).group()
            month_no = int(get_month_no_from_name(month))
            year_no = int(year.strip())
            days_in_month = calendar.monthrange(year_no, month_no)[1]
            start_date = datetime.date.today().replace(day=1, month=month_no, year=year_no)
            end_date = datetime.date.today().replace(day=days_in_month, month=month_no, year=year_no)
            start_end_date.append([start_date, end_date])
        return start_end_date

    def get_filter_date_min_max(self, months=None):
        if months:
            dates = self.get_start_end_date_month(months)
            sorted_end_dates = sorted([date[1] for date in dates])
            size = len(sorted_end_dates)
            return sorted_end_dates[size - 1], sorted_end_dates[size - 2] if size >= 2 else None
        else:
            today_date = datetime.date.today()
            return today_date + relativedelta(days=-1), today_date + relativedelta(months=-1, days=-1)

    def divide(self, numerator, denominator):
        try:
            return numerator / denominator
        except Exception:
            return 0

    def month_year_comparator(self, month_year):
        year = re.search("[0-9]+", month_year).group()
        month = re.search("[a-zA-z]+", month_year).group()
        month_no = int(get_month_no_from_name(month))
        year_no = int(year.strip())
        return year_no * 12 + month_no

    def month_year_comparator_graph(self, graph_data):
        month_year = graph_data['month']
        return self.month_year_comparator(month_year)

    @action(detail=False, methods=['GET'], url_path='level2/open-trips/source')
    def open_trips_source(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_open_trips_source_graph.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_open_trips_source_graph")
        response = []
        for each_result in result:
            if each_result[0]:
                each_source_data = dict()
                each_source_data['source'] = each_result[0]
                each_source_data['valid_trip_count'] = each_result[1]
                each_source_data['open_trip_count'] = each_result[2]
                each_source_data['open_trip_percent'] = round_off(each_result[3], 2)
                response.append(each_source_data)
        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/destination')
    def open_trips_destination(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_open_trips_destination_graph.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_open_trips_destination_graph")
        response = []
        for each_result in result:
            if each_result[0]:
                each_source_data = dict()
                each_source_data['destination'] = each_result[0]
                each_source_data['valid_trip_count'] = each_result[1]
                each_source_data['open_trip_count'] = each_result[2]
                each_source_data['open_trip_percent'] = round_off(each_result[3], 2)
                response.append(each_source_data)
        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/transporter')
    def open_trips_transporter(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_open_trips_transporter_graph.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_open_trips_transporter_graph")
        response = []
        for each_result in result:
            # each_source_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            if each_result[0]:
                each_source_data = dict()
                each_source_data["transporter_name"] = each_result[0]
                each_source_data["avg_days_to_deliver"] = round_off(each_result[1], 2)
                each_source_data["avg_distance_covered_kms"] = round_off(each_result[2], 2)
                each_source_data["valid_trip_count"] = each_result[3]
                each_source_data["open_trip_count"] = each_result[4]
                each_source_data["open_trip_perc"] = round_off(each_result[5], 2)
                response.append(each_source_data)

        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/age')
    def open_trips_age(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_open_trips_age_graph.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_open_trips_age_graph")
        response = dict()
        for each_result in result:
            each_source_data = dict()
            each_source_data["age_category"] = AGE_FILTERS_ORDER.get(each_result[0])
            each_source_data["valid_trip_count"] = each_result[1]
            each_source_data["open_trip_count"] = each_result[2]
            response[each_result[0]] = each_source_data
        actual_response = list()
        for each_age in AGE_FILTERS_ORDER.keys():
            if response.get(each_age):
                actual_response.append(response.get(each_age))
        return Response(data=actual_response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/calendar')
    def open_trips_calendar(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        current_year = datetime.date.today().year
        sql = queries.l2_open_trips_calendar.format(where=" where " + " and ".join(filters) if filters else '',
                                                    finance_year_start_date=f"{current_year - 1}-04-01")
        colnames, result = self.get_data_db(sql, "l2_open_trips_calendar")
        response = dict()
        response["year1"] = dict()
        response["year1"]["year"] = current_year - 1
        response["year1"]["data"] = list()
        response["year2"] = dict()
        response["year2"]["year"] = current_year
        response["year2"]["data"] = list()
        current_year = str(current_year)
        for each_result in result:
            date_of_dispach = each_result[0]
            year = str(date_of_dispach).split('-')[0]
            each_year_data = dict()
            each_year_data["date_of_dispach"] = each_result[0]
            each_year_data["valid_trip_count"] = each_result[1]
            each_year_data["open_trip_count"] = each_result[2]
            each_year_data["open_trip_perc"] = round_off(each_result[3], 2)
            if year == current_year:
                response["year2"]["data"].append(each_year_data)
            else:
                response["year1"]["data"].append(each_year_data)

        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/other-table')
    def open_trips_other_table(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_open_trips_other_table.format(where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_open_trips_other_table")
        response = []
        for each_result in result:
            each_source_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            each_source_data["per_day_km_travelled"] = int(round(each_source_data["per_day_km_travelled"], 0)) \
                if each_source_data["per_day_km_travelled"] else 0
            each_source_data["distance_covered_kms"] = int(round(each_source_data["distance_covered_kms"], 0)) \
                if each_source_data["distance_covered_kms"] else 0
            each_source_data["age_category"] = AGE_FILTERS_ORDER.get(each_source_data.get("age_category"))
            response.append(each_source_data)
        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/in-progress-table')
    def open_trips_in_progress_table(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")

        sql = queries.l3_open_trips_in_progress_table.format(where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_open_trips_in_progress_table")
        response = []
        for each_result in result:
            each_source_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            if each_source_data["pred_probability"]:
                each_source_data["pred_probability"] = str(
                    int(round_off(each_source_data["pred_probability"] * 100, 0))) + "%"
            else:
                each_source_data["pred_probability"] = IN_SUFFICIENT_DATA
            each_source_data["target_days_to_deliver"] = int(round(each_source_data["target_days_to_deliver"], 0)) \
                if each_source_data["target_days_to_deliver"] else 0
            each_source_data["distance"] = int(round_off(each_source_data["distance"], 0))
            each_source_data["distance_covered_kms"] = int(round_off(each_source_data["distance_covered_kms"], 0))
            each_source_data["avg_daily_distance"] = int(round_off(each_source_data["avg_daily_distance"], 0))
            each_source_data["avg_daily_distance_reqd"] = int(round_off(each_source_data["avg_daily_distance_reqd"], 0))
            response.append(each_source_data)
        return Response(data=response)

    def get_age_filter(self, age_filter_request):
        return AGE_FILTERS.get(age_filter_request)

    def format_l2_open_trips_filters(self, request, relation="", sec_relation=""):
        filters = {}
        age_filter = None
        days_to_deliver_filter = None
        avg_daily_distance_filter = None
        if request.GET.get('age'):
            age_filter = request.GET.get('age')
        if request.GET.get('days_to_deliver'):
            days_to_deliver_filter = request.GET.get('days_to_deliver')
        if request.GET.get('avg_daily_distance'):
            avg_daily_distance_filter = request.GET.get('avg_daily_distance')
        for k, v in request.GET.items():
            if k and v and v != '' and len(v) > 0:
                filters[k] = ",".join(["'{}'".format(each_value) for each_value in v.split(',')])
        months_input = None

        if filters.get('month'):
            months_input = filters.get('month')
            filters.pop('month')
        if filters.get('age'):
            filters.pop('age')
        if filters.get('days_to_deliver'):
            filters.pop('days_to_deliver')
        if filters.get('avg_daily_distance'):
            filters.pop('avg_daily_distance')

        # filters = ["{relation}{} in ({})".format(k, v, relation=relation) for k, v in filters.items()]
        temp = list()
        for k, v in filters.items():
            if k == "customer_name":
                temp.append("{relation}{} in ({})".format(k, v, relation=""))
            if k == "delay_category":
                temp.append("{relation}{} in ({})".format(k, v, relation=""))
            else:
                temp.append("{relation}{} in ({})".format(k, v, relation=relation))
        filters = temp
        if months_input:
            filters.append(self.generate_date_filter_query(months=months_input, relation=relation))
        if age_filter:
            filters.append(relation + self.get_age_filter(age_filter))
        if days_to_deliver_filter:
            filters.append(DAYS_TO_DELIVER_FILTER.get(days_to_deliver_filter).format(
                relation=sec_relation))  # Todo: relation value is hardcoded for this filter
        if avg_daily_distance_filter:
            filters.append(DAILY_DISTANCE_FILTER.get(avg_daily_distance_filter).format(relation=""))
        return filters

    def format_l3_open_trips_filters(self, request, relation=""):
        filters = {}
        age_input = None
        days_to_deliver_filter = None
        avg_daily_distance_filter = None
        #print(request.GET.get('age'))
        if request.GET.get('age'):
            age_input = request.GET.get('age')
        if request.GET.get('days_to_deliver'):
            days_to_deliver_filter = request.GET.get('days_to_deliver')
        if request.GET.get('avg_daily_distance'):
            avg_daily_distance_filter = request.GET.get('avg_daily_distance')

        for k, v in request.GET.items():
            if k and v and v != '' and len(v) > 0:
                filters[k] = ",".join(["'{}'".format(each_value) for each_value in v.split(',')])
        months_input = None
        date_input = None

        if filters.get('month'):
            months_input = filters.get('month')
            filters.pop('month')
        if filters.get('age'):
            filters.pop('age')
        if filters.get('date_of_dispach'):
            date_input = filters.get("date_of_dispach")
            filters.pop("date_of_dispach")
        if filters.get('days_to_deliver'):
            filters.pop('days_to_deliver')
        if filters.get('offset'):
            filters.pop('offset')
        if filters.get('avg_daily_distance'):
            filters.pop('avg_daily_distance')

        filters = ["{relation}{} in ({})".format(k, v, relation=relation) for k, v in filters.items()]
        if months_input:
            dates = self.get_start_end_date_month(months_input)
            template = "(day_and_time_of_dispach between '{start_date}' and '{end_date}')"
            date_filters = " OR ".join([template.format(start_date=date[0], end_date=date[1]) for date in dates])
            date_filters = "(" + date_filters + ")"
            filters.append(date_filters)
        if age_input:
            filters.append(AGE_FILTERS_L3.get(age_input).format(relation=relation))
        if date_input:
            filters.append("date({relation}day_and_time_of_dispach) in ({date_input})".format(date_input=date_input,
                                                                                              relation=relation))
        if days_to_deliver_filter:
            filters.append(DAYS_TO_DELIVER_FILTER.get(days_to_deliver_filter).format(
                relation=relation))  # Todo: relation value is hardcoded for this filter
        if avg_daily_distance_filter:
            filters.append(DAILY_DISTANCE_FILTER.get(avg_daily_distance_filter).format(relation="agg."))

        return filters

    @action(detail=False, methods=['GET'], url_path='filter-data')
    def get_filter_data(self, request):
        response = dict()
        sql = queries.l2_destination_filter
        colnames, result = self.get_data_db(sql, "l2_destination_filter")
        response["destination"] = [each_destination for each_destination in result]

        sql = queries.l2_source_filter
        colnames, result = self.get_data_db(sql, "l2_source_filter")
        response["source"] = [each_source for each_source in result]

        sql = queries.l2_date_filter
        colnames, result = self.get_data_db(sql, "l2_date_filter")
        dates = [" ".join(each_destination[0].split()) for each_destination in result]
        dates.sort(key=self.month_year_comparator)
        response["month"] = dates

        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/open-trips/min-max-dates')
    def min_max_record_l2_open_trips(self, request):
        sql = queries.max_min_date
        colnames, result = self.get_data_db(sql, "max_min_date")
        response = dict()
        response["max_date"] = result[0][0]
        response["min_date"] = result[0][1]
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/delayed-trips/source')
    def l2_delayed_trips_source(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_delayed_trips_source.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_delayed_trips_source")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/delayed-trips/destination')
    def l2_delayed_trips_destination(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_delayed_trips_destination.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_delayed_trips_destination")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/delayed-trips/transport')
    def l2_delayed_trips_transport(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_delayed_trips_transport.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_delayed_trips_transport")
        filters = self.format_l2_open_trips_filters(request, relation="vt.")
        graph_sql = queries.l2_delayed_trips_transport_graph.format(
            where=" where " + " and ".join(filters) if filters else '')
        graph_colnames, graph_result = self.get_data_db(graph_sql, "l2_delayed_trips_transport_graph")
        response = list()
        graph_data = dict()
        graph_result.sort(key=lambda tu: self.month_year_comparator(tu[3]))
        for each_graph_result in graph_result:
            if each_graph_result[0] not in graph_data:
                graph_data[each_graph_result[0]] = list()
            if each_graph_result[4]:
                graph_data[each_graph_result[0]].append(
                    {"month": each_graph_result[3], "delay_perc": each_graph_result[4]})

        for each_row in result:
            response_data = {colnames[itr]: round_off(each_row[itr], 0) for itr in range(0, len(each_row))}
            if graph_data.get(response_data["transporter_name"]):
                response_data["graph"] = graph_data.get(response_data["transporter_name"])
            else:
                response_data["graph"] = list()
            response.append(response_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/delayed-trips/calendar')
    def l2_delayed_trips_calendar(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="vt.")
        current_year = datetime.date.today().year
        sql = queries.l2_delayed_trips_calendar.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_delayed_trips_calendar")

        response = dict()
        response["year1"] = dict()
        response["year1"]["year"] = current_year - 1
        response["year1"]["data"] = list()
        response["year2"] = dict()
        response["year2"]["year"] = current_year
        response["year2"]["data"] = list()
        current_year = str(current_year)
        for each_result in result:
            date_of_dispach = each_result[0]
            year = str(date_of_dispach).split('-')[0]
            each_year_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            if year == current_year:
                response["year2"]["data"].append(each_year_data)
            else:
                response["year1"]["data"].append(each_year_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/delayed-trips/avg-daily-distance')
    def l2_delayed_trips_avg_distance(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="")
        response = dict()
        sql_delayed = queries.l2_delayed_avg_daily_distance_delayed.format(where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql_delayed, "l2_delayed_avg_daily_distance_delayed")
        try:
            response["avg_daily_distance_delay"] = round(result[0][0], 2)
        except KeyError:
            response["avg_daily_distance_delay"] = None

        sql_non_delayed = queries.l2_delayed_avg_daily_distance_non_delayed.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql_non_delayed, "l2_delayed_avg_daily_distance_non_delayed")
        try:
            response["avg_daily_distance_non_delay"] = round(result[0][0], 2)
        except KeyError:
            response["avg_daily_distance_non_delay"] = None
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/transporter')
    def l3_delayed_trips_transporter(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="")
        sql = queries.l3_delayed_trips_transporter_table.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_transporter_table")
        response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            each_data["delayed_avg_daily_distance"] = round_off(each_data["delayed_avg_daily_distance"], 1)
            each_data["non_delayed_avg_daily_distance"] = round_off(each_data["non_delayed_avg_daily_distance"], 1)
            each_data["amount_of_delay"] = str(round_off(each_data["amount_of_delay"], 1))
            each_data["delay_perc"] = round_off(each_data["delay_perc"], 2)
            response.append(each_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/info')
    def l3_delayed_trips_info(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_delayed_trips_info_table.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_info_table")
        response = list()
        s_no = 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/fastest-route')
    def l3_delayed_trips_fastest_route(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_delayed_trips_fastest_route.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_fastest_route")
        response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            response.append(each_data)

        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/shortest-route')
    def l3_delayed_trips_shortest_route(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_delayed_trips_shortest_route.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_shortest_route")
        response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            response.append(each_data)

        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/greenest-route')
    def l3_delayed_trips_greenest_route(self, request):
        filters = self.format_l3_open_trips_filters(request)
        sql = queries.l3_delayed_trips_greenest_route.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_greenest_route")
        response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            response.append(each_data)

        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/best-transporter')
    def l3_delayed_trips_best_transporter(self, request):
        filters = self.format_l3_open_trips_filters(request)
        sql = queries.l3_delayed_trips_best_transporter.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_best_transporter")
        response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            response.append(each_data)

        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/closed-trips/source')
    def l2_closed_trips_source(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_closed_trips_source.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_closed_trips_source")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/closed-trips/destination')
    def l2_closed_trips_destination(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="", sec_relation="")
        sql = queries.l2_closed_trips_destination.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_closed_trips_destination")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/closed-trips/transporter')
    def l2_closed_trips_transporter(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="", sec_relation="")
        sql = queries.l2_closed_trips_transporter.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_closed_trips_transporter")

        filters = self.format_l2_open_trips_filters(request, relation="vt.", sec_relation="ct.")
        graph_sql = queries.l2_closed_trips_transporter_graph.format(
            where=" where " + " and ".join(filters) if filters else '')
        graph_colnames, graph_result = self.get_data_db(graph_sql, "l2_closed_trips_transporter_graph")
        response = list()
        graph_data = dict()
        graph_result.sort(key=lambda tu: self.month_year_comparator(tu[3]))
        for each_graph_result in graph_result:
            if each_graph_result[0] not in graph_data:
                graph_data[each_graph_result[0]] = list()
            if each_graph_result[4]:
                graph_data[each_graph_result[0]].append(
                    {"month": each_graph_result[3], "close_perc": each_graph_result[4]})

        for each_row in result:
            response_data = {colnames[itr]: round_off(each_row[itr], 0) for itr in range(0, len(each_row))}
            if graph_data.get(response_data["transporter_name"]):
                response_data["graph"] = graph_data.get(response_data["transporter_name"])
            else:
                response_data["graph"] = list()
            response.append(response_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/closed-trips/days-to-deliver')
    def l2_closed_trips_days_to_deliver(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="")
        sql = queries.l2_closed_trips_day_to_deliver.format(where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_closed_trips_day_to_deliver")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))})

        sorted_response = []
        last_item = {}

        for i in range(0, 10):
            for item in response:
                if (item["days_to_deliver_category"][0] == str(i)):
                    sorted_response.append(item)
                if (item["days_to_deliver_category"][0] == ">"):
                    last_item = item

        sorted_response.append(last_item)
        if(sorted_response[1]["days_to_deliver_category"] == "0"):
            sorted_response[0], sorted_response[1] = sorted_response[1], sorted_response[0]
        return Response(sorted_response)

    @action(detail=False, methods=['get'], url_path='level2/closed-trips/calendar')
    def l2_closed_trips_calendar(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="", sec_relation="")
        current_year = datetime.date.today().year
        sql = queries.l2_closed_trips_calendar.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_closed_trips_calendar")
        response = dict()
        response["year1"] = dict()
        response["year1"]["year"] = current_year - 1
        response["year1"]["data"] = list()
        response["year2"] = dict()
        response["year2"]["year"] = current_year
        response["year2"]["data"] = list()
        current_year = str(current_year)
        for each_result in result:
            date_of_dispach = each_result[0]
            year = str(date_of_dispach).split('-')[0]
            each_year_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            if year == current_year:
                response["year2"]["data"].append(each_year_data)
            else:
                response["year1"]["data"].append(each_year_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/closed-trips/info')
    def l3_closed_trips_info(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_closed_trips_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="limit 200",
            offset=format_offset(offset))
        colnames, result = self.get_data_db(sql, "l3_closed_trips_info")
        response = list()
        s_no = int(offset) if offset else 0
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/closed-trips/info-download')
    def l3_closed_trips_info_download(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_closed_trips_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="",
            offset="")
        colnames, result = self.get_data_db(sql, "l3_closed_trips_info")
        response = list()
        s_no = 0
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return populate_xlxs_from_data(colnames, result, "closed trip info")

    @action(detail=False, methods=['get'], url_path='level3/open-trips/download')
    def open_trips_l3_download(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")

        sql = queries.l3_open_trips_in_progress_table.format(where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_open_trips_in_progress_table")
        in_progress_response = []
        for each_result in result:
            each_source_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            if each_source_data["pred_probability"]:
                each_source_data["pred_probability"] = str(
                    int(round_off(each_source_data["pred_probability"] * 100, 0))) + "%"
            else:
                each_source_data["pred_probability"] = IN_SUFFICIENT_DATA
            each_source_data["target_days_to_deliver"] = int(round(each_source_data["target_days_to_deliver"], 0)) \
                if each_source_data["target_days_to_deliver"] else 0
            each_source_data["distance"] = int(round_off(each_source_data["distance"], 0))
            each_source_data["distance_covered_kms"] = int(round_off(each_source_data["distance_covered_kms"], 0))
            each_source_data["avg_daily_distance"] = int(round_off(each_source_data["avg_daily_distance"], 0))
            each_source_data["avg_daily_distance_reqd"] = int(round_off(each_source_data["avg_daily_distance_reqd"], 0))
            in_progress_response.append(each_source_data)

        sql = queries.l3_open_trips_other_table.format(where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_open_trips_other_table")
        other_table_response = []
        for each_result in result:
            each_source_data = {colnames[itr]: each_result[itr] for itr in range(0, len(each_result))}
            each_source_data["per_day_km_travelled"] = int(round(each_source_data["per_day_km_travelled"], 0)) \
                if each_source_data["per_day_km_travelled"] else 0
            each_source_data["distance_covered_kms"] = int(round(each_source_data["distance_covered_kms"], 0)) \
                if each_source_data["distance_covered_kms"] else 0
            each_source_data["age_category"] = AGE_FILTERS_ORDER.get(each_source_data.get("age_category"))
            other_table_response.append(each_source_data)
        return populate_xlxs_from_dict_data([in_progress_response, other_table_response], "open trips",
                                            ["in progress", "other"])

    @action(detail=False, methods=['get'], url_path='level3/delayed-trips/download')
    def l3_delayed_trips_download(self, request):
        filters = self.format_l3_open_trips_filters(request)
        sql = queries.l3_delayed_trips_best_transporter.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_best_transporter")
        best_transporter_response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            best_transporter_response.append(each_data)

        filters = self.format_l3_open_trips_filters(request, relation="main_table.")
        sql = queries.l3_delayed_trips_transporter_table.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_transporter_table")
        transporter_table_responseresponse = list()
        s_no = 1
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            each_data["delayed_avg_daily_distance"] = round_off(each_data["delayed_avg_daily_distance"], 1)
            each_data["non_delayed_avg_daily_distance"] = round_off(each_data["non_delayed_avg_daily_distance"], 1)
            each_data["amount_of_delay"] = str(round_off(each_data["amount_of_delay"], 1))
            transporter_table_responseresponse.append(each_data)
            s_no += 1

        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_delayed_trips_info_table.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_info_table")
        info_table_response = list()
        s_no = 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            info_table_response.append(each_data)
            s_no += 1

        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_delayed_trips_fastest_route.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_fastest_route")
        fastest_route_response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            fastest_route_response.append(each_data)

        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        sql = queries.l3_delayed_trips_shortest_route.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_shortest_route")
        shortest_route_response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            shortest_route_response.append(each_data)

        filters = self.format_l3_open_trips_filters(request)
        sql = queries.l3_delayed_trips_greenest_route.format(
            where=" and " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l3_delayed_trips_greenest_route")
        greenest_route_response = list()
        for each_row in result:
            each_data = {colnames[itr]: each_row[itr] for itr in range(0, len(each_row))}
            greenest_route_response.append(each_data)

        return populate_xlxs_from_dict_data([transporter_table_responseresponse,
                                             info_table_response, fastest_route_response, shortest_route_response,
                                             greenest_route_response, best_transporter_response],
                                            "delayed trips",
                                            ["best_transporter", "transporter_table",
                                             "info_table", "fastest_route",
                                             "shortest_route", "greenest_route"])

    @action(detail=False, methods=['get'], url_path='level2/forceful-trips/source')
    def l2_forceful_trips_source(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_forceful_closure_trips_source.format(
            where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_forceful_closure_trips_source")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/forceful-trips/destination')
    def l2_forceful_trips_destination(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_forceful_closure_trips_destination.format(
            where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_forceful_closure_trips_destination")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/forceful-trips/customer')
    def l2_forceful_trips_customer(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_forceful_closure_trips_customer.format(
            where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_forceful_closure_trips_customer")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})

        refined_response = {}
        for item in response:
            if item["customer_name"] in refined_response:
                # refined_response[item["customer_name"]["graph_data"]]
                temp_list = refined_response[item["customer_name"]]["graph"]
                temp_list.append({
                        "transporter_name": item["transporter_name"],
                        "close_forcefull_trip_trans": item["close_forcefull_trip_trans"]
                    })

                refined_response[item["customer_name"]]["graph"] = temp_list
            else:
                refined_response[item["customer_name"]] = {
                    "close_trip": item["close_trip"],
                    "close_forcefull_trip": item["close_forcefull_trip"],
                    "forcefull_perc": item["forcefull_perc"],
                    "graph":[{
                        "transporter_name": item["transporter_name"],
                        "close_forcefull_trip_trans": item["close_forcefull_trip_trans"]
                    }]
                }
        final_refined_response = []

        for key in refined_response:
            final_refined_response.append(
                {
                    "customer_name": key,
                    **refined_response[key]
                }
            )
        return Response(final_refined_response)
        # return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/forceful-trips/calendar')
    def l2_forceful_trips_calendar(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_forceful_closure_trips_calendar.format(
            where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_forceful_closure_trips_calendar")
        current_year = datetime.date.today().year
        response = dict()
        response["year1"] = dict()
        response["year1"]["year"] = current_year - 1
        response["year1"]["data"] = list()
        response["year2"] = dict()
        response["year2"]["year"] = current_year
        response["year2"]["data"] = list()
        current_year = str(current_year)
        for each_result in result:
            date_of_dispach = each_result[0]
            year = str(date_of_dispach).split('-')[0]
            each_year_data = dict()
            each_year_data["date_of_dispach"] = each_result[0]
            each_year_data["valid_trip_count"] = each_result[1]
            each_year_data["close_trip"] = each_result[2]
            each_year_data["forceful_trip"] = each_result[3]
            each_year_data["forceful_trip_perc"] = each_result[4]
            if year == current_year:
                response["year2"]["data"].append(each_year_data)
            else:
                response["year1"]["data"].append(each_year_data)

        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level3/forceful-trips/info')
    def l3_forceful_trips_info(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_forceful_closure_trips_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="limit 200",
            offset=format_offset(offset))
        colnames, result = self.get_data_db(sql, "l3_forceful_closure_trips_info")
        response = list()
        s_no = int(offset)+1 if offset else 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/forceful-trips/info-download')
    def l3_forceful_trips_info_download(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_forceful_closure_trips_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="",
            offset="")
        colnames, result = self.get_data_db(sql, "l3_forceful_closure_trips_info")
        response = list()
        s_no = int(offset)+1 if offset else 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return populate_xlxs_from_dict_data([response], filename="forcecul closure trip", sheet_names=["trip info"])

    @action(detail=False, methods=['get'], url_path='level2/days-to-deliver/source')
    def l2_days_to_deliver_source(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_days_to_deliver_source.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_days_to_deliver_source")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/days-to-deliver/destination')
    def l2_days_to_deliver_destination(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_days_to_deliver_destination.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_days_to_deliver_destination")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/days-to-deliver/transporter')
    def l2_days_to_deliver_transporter(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_days_to_deliver_transporter.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_days_to_deliver_transporter")
        # filters = self.format_l2_open_trips_filters(request, relation="vt.", sec_relation="")
        graph_sql = queries.l2_days_to_deliver_transporter_graph.format(
            where=" where " + " and ".join(filters) if filters else '')
        graph_colnames, graph_result = self.get_data_db(graph_sql, "l2_days_to_deliver_transporter_graph")
        response = list()
        graph_data = dict()
        graph_result.sort(key=lambda tu: self.month_year_comparator(tu[2]))
        for each_graph_result in graph_result:
            if each_graph_result[0] not in graph_data:
                graph_data[each_graph_result[0]] = list()
            if each_graph_result[2]:
                graph_data[each_graph_result[0]].append(
                    {"month": each_graph_result[2], "avg_days_deliver": round_off(each_graph_result[1], 2)})

        for each_row in result:
            response_data = {colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))}
            if graph_data.get(response_data["transporter_name"]):
                response_data["graph"] = graph_data.get(response_data["transporter_name"])
            else:
                response_data["graph"] = list()
            response.append(response_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/days-to-deliver/avg')
    def l2_days_to_deliver_avg(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_days_to_deliver_avg.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_days_to_deliver_avg")
        response = dict()

        close_trip_count = dict()
        for each_row in result:
            if each_row[0] in close_trip_count:
                close_trip_count[each_row[0]] += each_row[2]
            else:
                close_trip_count[each_row[0]] = each_row[2]
        for each_row in result:  # Todo: can be optimised
            if each_row[0] not in response:
                response[each_row[0]] = dict()
                response[each_row[0]]['delay_category'] = each_row[0]
            response[each_row[0]]["{}_close_trip".format(each_row[1])] = each_row[2]
            response[each_row[0]]["{}_close_trip_perc".format(each_row[1])] = \
                round_off(each_row[2] * 100 / close_trip_count[each_row[0]])

            # response.append({colnames[itr]: each_row[itr] for itr in range(0, len(each_row))})
        response = [value for value in response.values()]
        sorted_response = []
        last_item = {}

        for i in range(0, 10):
            for item in response:
                obj = {}
                obj["delay_category"] = item["delay_category"]

                if ("early_close_trip" not in item):
                    item["early_close_trip"] = ""

                obj["early_close_trip"] = item["early_close_trip"]

                if ("early_close_trip_perc" not in item):
                    item["early_close_trip_perc"] = ""

                obj["early_close_trip_perc"] = item["early_close_trip_perc"]

                if ("on_time_close_trip" not in item):
                    item["on_time_close_trip"] = ""

                obj["on_time_close_trip"] = item["on_time_close_trip"]

                if ("on_time_close_trip_perc" not in item):
                    item["on_time_close_trip_perc"] = ""

                obj["on_time_close_trip_perc"] = item["on_time_close_trip_perc"]

                if ("delayed_close_trip" not in item):
                    item["delayed_close_trip"] = ""

                obj["delayed_close_trip"] = item["delayed_close_trip"]

                if ("delayed_close_trip_perc" not in item):
                    item["delayed_close_trip_perc"] = ""

                obj["delayed_close_trip_perc"] = item["delayed_close_trip_perc"]

                if (item["delay_category"][0] == str(i)):
                    sorted_response.append(obj)

                if (item["delay_category"][0] == ">"):
                    last_item = obj

        sorted_response.append(last_item)

        if len(sorted_response) > 1:
            if (sorted_response[1]["delay_category"] == "0"):
                sorted_response[0], sorted_response[1] = sorted_response[1], sorted_response[0]

        return Response(sorted_response)

    @action(detail=False, methods=['get'], url_path='level2/days-to-deliver/calendar')
    def l2_days_to_deliver_calendar(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_days_to_deliver_calendar.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_days_to_deliver_calendar")
        current_year = datetime.date.today().year
        response = dict()
        response["year1"] = dict()
        response["year1"]["year"] = current_year - 1
        response["year1"]["data"] = list()
        response["year2"] = dict()
        response["year2"]["year"] = current_year
        response["year2"]["data"] = list()
        current_year = str(current_year)
        for each_result in result:
            date_of_dispach = each_result[0]
            year = str(date_of_dispach).split('-')[0]
            each_year_data = dict()
            each_year_data["date_of_dispach"] = each_result[0]
            each_year_data["close_trip"] = each_result[1]
            each_year_data["avg_days_deliver"] = round_off(each_result[2], 2)
            if year == current_year:
                response["year2"]["data"].append(each_year_data)
            else:
                response["year1"]["data"].append(each_year_data)

        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level3/days-to-deliver/info')
    def l3_days_to_deliver_info(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_days_to_deliver_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="limit 200",
            offset=format_offset(offset))
        colnames, result = self.get_data_db(sql, "l3_days_to_deliver_info")
        response = list()
        s_no = int(offset)+1 if offset else 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/days-to-deliver/info-download')
    def l3_days_to_deliver_info_download(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_days_to_deliver_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="",
            offset="")
        colnames, result = self.get_data_db(sql, "l3_days_to_deliver_info")
        response = list()
        s_no = int(offset)+1 if offset else 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return populate_xlxs_from_dict_data([response], filename="Average Days to Deliver", sheet_names=["trip info"])

    @action(detail=False, methods=['get'], url_path='level2/daily-distance/source')
    def l2_daily_distance_source(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_daily_distance_source.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_daily_distance_source")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/daily-distance/destination')
    def l2_daily_distance_destination(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_daily_distance_destination.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_daily_distance_destination")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: round_off(each_row[itr], 2) for itr in range(0, len(each_row))})
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/daily-distance/transporter')
    def l2_daily_distance_transporter(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_daily_distance_transporter.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_daily_distance_transporter")
        graph_sql = queries.l2_daily_distance_transporter_graph.format(
            where=" where " + " and ".join(filters) if filters else '')
        graph_colnames, graph_result = self.get_data_db(graph_sql, "l2_daily_distance_transporter_graph")
        response = list()
        graph_data = dict()
        graph_result.sort(key=lambda tu: self.month_year_comparator(tu[2]))
        for each_graph_result in graph_result:
            if each_graph_result[0] not in graph_data:
                graph_data[each_graph_result[0]] = list()
            if each_graph_result[2]:
                graph_data[each_graph_result[0]].append(
                    {"month": each_graph_result[2], "avg_days_deliver": round_off(each_graph_result[1], 2)})

        for each_row in result:
            response_data = {colnames[itr]: round_off(each_row[itr], 0) for itr in range(0, len(each_row))}
            if graph_data.get(response_data["transporter_name"]):
                response_data["graph"] = graph_data.get(response_data["transporter_name"])
            else:
                response_data["graph"] = list()
            response.append(response_data)
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level2/daily-distance/calendar')
    def l2_daily_distance_calendar(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_daily_distance_calendar.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_daily_distance_calendar")
        current_year = datetime.date.today().year
        response = dict()
        response["year1"] = dict()
        response["year1"]["year"] = current_year - 1
        response["year1"]["data"] = list()
        response["year2"] = dict()
        response["year2"]["year"] = current_year
        response["year2"]["data"] = list()
        current_year = str(current_year)
        for each_result in result:
            date_of_dispach = each_result[0]
            year = str(date_of_dispach).split('-')[0]
            each_year_data = dict()
            each_year_data["date_of_dispach"] = each_result[0]
            each_year_data["close_trip"] = each_result[1]
            each_year_data["avg_daily_distance"] = round_off(each_result[2], 2)
            if year == current_year:
                response["year2"]["data"].append(each_year_data)
            else:
                response["year1"]["data"].append(each_year_data)

        return Response(data=response)

    @action(detail=False, methods=['get'], url_path='level2/daily-distance/avg')
    def l2_daily_distance_avg(self, request):
        filters = self.format_l2_open_trips_filters(request, relation="")
        sql = queries.l2_daily_distance_avg.format(where=" where " + " and ".join(filters) if filters else '')
        colnames, result = self.get_data_db(sql, "l2_daily_distance_avg")
        response = list()
        for each_row in result:
            response.append({colnames[itr]: round_off(each_row[itr],2) for itr in range(0, len(each_row))})

        sorted_response = []
        last_item = {}

        for i in range(0, 10):
            for item in response:
                if (item["distance_covered_kms_category"].split("-")[0] == str(i*50)):
                    sorted_response.append(item)
                if (item["distance_covered_kms_category"][0] == ">"):
                    last_item = item

        sorted_response.append(last_item)

        if len(sorted_response) > 1:
            if (sorted_response[1]["distance_covered_kms_category"] == "0"):
                sorted_response[0], sorted_response[1] = sorted_response[1], sorted_response[0]
        return Response(sorted_response)


    @action(detail=False, methods=['get'], url_path='level3/daily-distance/info')
    def l3_daily_distance_info(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_daily_distance_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="limit 200",
            offset=format_offset(offset))
        colnames, result = self.get_data_db(sql, "l3_daily_distance_info")
        response = list()
        s_no = int(offset)+1 if offset else 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return Response(response)

    @action(detail=False, methods=['get'], url_path='level3/daily-distance/info-download')
    def l3_daily_distance_info_download(self, request):
        filters = self.format_l3_open_trips_filters(request, relation="agg.")
        offset = request.GET.get('offset', '')
        sql = queries.l3_forceful_closure_trips_info.format(
            where=" and " + " and ".join(filters) if filters else '',
            limit="",
            offset="")
        colnames, result = self.get_data_db(sql, "l3_daily_distance_info")
        response = list()
        s_no = int(offset)+1 if offset else 1
        for each_row in result:
            each_data = {colnames[itr]: round_off(each_row[itr]) for itr in range(0, len(each_row))}
            each_data["s_no"] = s_no
            response.append(each_data)
            s_no += 1
        return populate_xlxs_from_dict_data([response], filename="Average Daily Distance", sheet_names=["trip info"])