LAST_MONTH_TILL_END_FILTER = """date(day_and_time_of_dispach) between date(date_trunc('month', CURRENT_DATE)-'1 month'::interval)
and date( date_trunc('month', CURRENT_DATE) - '1 day'::interval)"""

LAST_MONTH_FILTER = """date(day_and_time_of_dispach) between date(date_trunc('month', CURRENT_DATE-1)-'1 month'::interval) 
and date((CURRENT_DATE-1)-'1 month'::interval)"""

CURRENT_MONTH_FILTER = """date(day_and_time_of_dispach) between date( date_trunc('month', CURRENT_DATE-1)) and date(CURRENT_DATE-1)"""

GREEN = "green"
RED = "red"

LIT_SOURCE = ('ADITYA', 'ALUPURAM', 'BELUR', 'HIRAKUD', 'MAHAN', 'MOUDA', 'RENUKOOT', 'TALOJA')

IN_PROGRESS = "In Progress"
ONE_DAY_LATE = "1 Day Late"
ONE_TO_FIFTEEN_DAY_LATE = "1 to 15 Days Late"
FIFTEEN_TO_THIRTY_DAY_LATE = "15 to 30 Days Late"
THIRTY_TO_NINETY_DAY_LATE = "30 to 90 Days Late"
GREATER_THAN_90_DAY_LATE = ">90 Days Late"

AGE_FILTERS = {
    IN_PROGRESS: "age_category = 'IN_PROGRESS'",
    ONE_DAY_LATE: "age_category = '1_DAY_LATE'",
    ONE_TO_FIFTEEN_DAY_LATE: "age_category = '1_TO_15_DAY_LATE'",
    FIFTEEN_TO_THIRTY_DAY_LATE: "age_category = '15_TO_30_DAY_LATE'",
    THIRTY_TO_NINETY_DAY_LATE: "age_category = '30_TO_90_DAY_LATE'",
    GREATER_THAN_90_DAY_LATE: "age_category = '>90_DAY_LATE'"
}
AGE_FILTERS_ORDER = {
    "IN_PROGRESS": "In Progress",
    "1_DAY_LATE": "1 Day Late",
    "1_TO_15_DAY_LATE": "1 to 15 Days Late",
    "15_TO_30_DAY_LATE": "15 to 30 Days Late",
    "30_TO_90_DAY_LATE": "30 to 90 Days Late",
    ">90_DAY_LATE": ">90 Days Late",
}

AGE_FILTERS_L3 = {
    IN_PROGRESS: "({relation}over_due_days - ({relation}google_distance/300)) < 1",
    ONE_DAY_LATE: """({relation}over_due_days - ({relation}google_distance/300)) >=1 and
    ({relation}over_due_days - ({relation}google_distance/300)) < 2""",
    ONE_TO_FIFTEEN_DAY_LATE: "({relation}over_due_days - ({relation}google_distance/300)) >= 2 and "
                             "({relation}over_due_days - ({relation}google_distance/300)) < 16",
    FIFTEEN_TO_THIRTY_DAY_LATE: "({relation}over_due_days - ({relation}google_distance/300)) >= 16 and"
                                "({relation}over_due_days - ({relation}google_distance/300)) < 31",
    THIRTY_TO_NINETY_DAY_LATE: "({relation}over_due_days - ({relation}google_distance/300)) >= 31 and"
                                "({relation}over_due_days - ({relation}google_distance/300)) < 91",
    GREATER_THAN_90_DAY_LATE: "(({relation}over_due_days - ({relation}google_distance/300)) >= 91 or ({relation}over_due_days - ({relation}google_distance/300)) is null)"
}

# AGE_FILTERS_L3 = {
#     IN_PROGRESS: "age_category='IN_PROGRESS'",
#     ONE_DAY_LATE: "age_category='1_DAY_LATE'",
#     ONE_TO_FIFTEEN_DAY_LATE: "age_category='1_TO_15_DAY_LATE'",
#     FIFTEEN_TO_THIRTY_DAY_LATE: "age_category='15_TO_30_DAY_LATE'",
#     THIRTY_TO_NINETY_DAY_LATE: "age_category='30_TO_90_DAY_LATE'",
#     GREATER_THAN_90_DAY_LATE: "age_category='>90_DAY_LATE'"
# }

IN_SUFFICIENT_DATA = "In sufficient data"

DELAYED = "DELAYED"
ONE_DAY_DELAY = "ONE_DAY_DELAY"
EARLY = "EARLY"
ONE_DAY_EARLY = "ONE_DAY_EARLY"
ON_TIME = "ON_TIME"
DELAYED_CATEGORY = [DELAYED, ONE_DAY_DELAY]
NON_DELAYED_CATEGORY = [EARLY, ONE_DAY_EARLY, ON_TIME]

ZERO_DAYS_TO_DELIVER = "0 DAYS TO DELIVER"
LESS_THAN_1_DAYS_TO_DELIVER = "< 1 DAYS TO DELIVER"
LESS_THAN_2_DAYS_TO_DELIVER = "< 2 DAYS TO DELIVER"
LESS_THAN_3_DAYS_TO_DELIVER = "< 3 DAYS TO DELIVER"
LESS_THAN_4_DAYS_TO_DELIVER = "< 4 DAYS TO DELIVER"
LESS_THAN_5_DAYS_TO_DELIVER = "< 5 DAYS TO DELIVER"
LESS_THAN_6_DAYS_TO_DELIVER = "< 6 DAYS TO DELIVER"
LESS_THAN_7_DAYS_TO_DELIVER = "< 7 DAYS TO DELIVER"
LESS_THAN_8_DAYS_TO_DELIVER = "< 8 DAYS TO DELIVER"
GREATER_THAN_8 = "> 8"

DAYS_TO_DELIVER_FILTER = {
    ZERO_DAYS_TO_DELIVER: "{relation}eta  = 0",
    LESS_THAN_1_DAYS_TO_DELIVER: "{relation}eta >= 0 and {relation}eta<1",
    LESS_THAN_2_DAYS_TO_DELIVER: "{relation}eta >= 1 and {relation}eta<2",
    LESS_THAN_3_DAYS_TO_DELIVER: "{relation}eta >= 2 and {relation}eta<3",
    LESS_THAN_4_DAYS_TO_DELIVER: "{relation}eta >= 3 and {relation}eta<4",
    LESS_THAN_5_DAYS_TO_DELIVER: "{relation}eta >= 4 and {relation}eta<5",
    LESS_THAN_6_DAYS_TO_DELIVER: "{relation}eta >= 5 and {relation}eta<6",
    LESS_THAN_7_DAYS_TO_DELIVER: "{relation}eta >= 6 and {relation}eta<7",
    LESS_THAN_8_DAYS_TO_DELIVER: "{relation}eta >= 7 and {relation}eta<8",
    GREATER_THAN_8: "{relation}eta > 8"
}

ZERO_DISTANCE_COVERED = '0'
ZERO_TO_FIFTY_DISTANCE_COVERED = '0-50'
FIFTY_TO_HUNDRED_DISTANCE_COVERED = '50-100'
HUNDRED_TO_ONE_HUNDRED_FIFTY_DISTANCE_COVERED = '100-150'
ONE_HUNDRED_FIFTY_TO_TWO_HUNDRED_DISTANCE_COVERED = '150-200'
TWO_HUNDRED_TO_TWO_HUNDRED_FIFTY_DISTANCE_COVERED = '200-250'
TWO_HUNDRED_FIFTY_TO_THREE_HUNDRED_DISTANCE_COVERED = '250-300'
GREATER_THAN_THREE_HUNDRED_DISTANCE_COVERED = '>300'

DAILY_DISTANCE_FILTER = {
    ZERO_DISTANCE_COVERED: '{relation}distance_covered_kms = 0',
    ZERO_TO_FIFTY_DISTANCE_COVERED: '{relation}distance_covered_kms > 0  and {relation}distance_covered_kms <= 50',
    FIFTY_TO_HUNDRED_DISTANCE_COVERED: '{relation}distance_covered_kms > 50  and {relation}distance_covered_kms <= 100',
    HUNDRED_TO_ONE_HUNDRED_FIFTY_DISTANCE_COVERED: '{relation}distance_covered_kms > 100  and {'
                                                   'relation}distance_covered_kms <= 150',
    ONE_HUNDRED_FIFTY_TO_TWO_HUNDRED_DISTANCE_COVERED: '{relation}distance_covered_kms > 150  and {'
                                                       'relation}distance_covered_kms <= '
                                                       '200',
    TWO_HUNDRED_TO_TWO_HUNDRED_FIFTY_DISTANCE_COVERED: '{relation}distance_covered_kms > 200  and {'
                                                       'relation}distance_covered_kms <= '
                                                       '250 THEN',
    TWO_HUNDRED_FIFTY_TO_THREE_HUNDRED_DISTANCE_COVERED: '{relation}distance_covered_kms > 250  and {'
                                                         'relation}distance_covered_kms '
                                                         '<= 300',
    GREATER_THAN_THREE_HUNDRED_DISTANCE_COVERED: '{relation}distance_covered_kms > 300'
}
