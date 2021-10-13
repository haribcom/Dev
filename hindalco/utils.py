import datetime
import psycopg2
import os


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


def format_offset(offset):
    if offset:
        return "offset " + str(offset)
    return ""
