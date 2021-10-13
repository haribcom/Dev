total_trips_graph = """select month, count(distinct trip_no) as trip_no 
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
{where} group by 1"""

valid_trips_graph = """select month, count(distinct trip_no) as trip_no
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
{where} group by 1"""

open_trips_graph = """select month,count(distinct trip_no) as trip_no
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'OPEN' {where} group by 1;"""

closed_trips_graph = """select month, count(distinct trip_no) as trip_no from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' {where} group by 1; """

geofence_closures_graph = """select month, count(distinct trip_no) as trip_no from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and closer_remarks='geofence' {where} group by 1; """

forceful_closures_graph = """select month, count(distinct trip_no) as trip_no from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz where 
(invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and (closer_remarks = 'forcefull_closure' OR closer_remarks is null) {where} group by 1; """

delay_trips_graph = """select month, count(distinct trip_no) as trip_no from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY') {where} group by 1; """

avg_daily_distance = """select month, avg(per_day_km_travelled * 1.0)  as per_day from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' {where} group by 1; """

avg_total_daily_distance = """select avg(per_day_km_travelled * 1.0)  as per_day from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' {where};"""

avg_days_deliver_graph = """select month, avg(eta * 1.0)  as per_day from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' {where} group by 1 ; """

avg_total_days_deliver = """select avg(eta * 1.0)  as per_day from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' {where};"""

carbon_emission_graph = """select month, sum(carbon_emission)  as per_day from 
dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' {where} group by 1 ; """

###################################################################################################

# -- total trip in last month till today's date
total_trips_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where  {where}"""

# -- total trip in this month
total_trips_count_curr_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where  {where}
"""

# -- total valid trip in last month till today's date
valid_trips_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and 
(invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)"""

# -- total valid trip in this month
valid_trips_count_this_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and 
(invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)"""

# -- total valid and open trip in last month till today's date
open_trips_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED'"""

# -- total valid and open trip in this month
open_trips_count_this_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and ( invalid_flag IS NULL or invalid_flag='TRANSIT_HOURS_IS_HIGHER' or invalid_flag='TRANSIT_HOURS_IS_NOT_CORRECT')
 and trip_status = 'OPEN'"""

# -- total valid and closed trip in last month till today's date
closed_trips_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' """

# -- total valid and closed trip in this month
closed_trips_count_this_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and  (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED'"""

# -- total valid and closed trip remark geofence in last month till today's date
geofence_closures_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and closer_remarks='geofence' 
"""

# -- total valid and closed trip remark geofence in this month
geofence_closures_count_this_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and closer_remarks='geofence'"""

# -- total valid and closed trip remark forcefull_closure in last month till today's date
forceful_closures_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)  
and trip_status = 'CLOSED' and (closer_remarks = 'forcefull_closure' OR closer_remarks is null)'"""


# -- total valid and closed trip remark forcefull_closure in this month
forceful_closures_count_this_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)   
and trip_status = 'CLOSED' and (closer_remarks = 'forcefull_closure' OR closer_remarks is null)'"""

# -- total valid and closed trip remark delay in last month till today's date
delay_trips_count_last_month = """select count(distinct trip_no) tota_trips_prev_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY')"""

# -- total valid and closed trip remark delay in this month
delay_trips_count_this_month = """select count(distinct trip_no) tota_trips_this_month
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY')"""

# -- average per_day_km_travelled valid and closed trip remark delay in last month till today's date
avg_daily_distance_count_last_month = """select avg(per_day_km_travelled * 1.0)  as per_day
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' """

# -- average per_day_km_travelled valid and closed trip remark delay in this month
avg_daily_distance_count_this_month = """select avg(per_day_km_travelled * 1.0)  as per_day
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' """

# -- average eta valid and closed trip remark delay in last month till today's date
avg_days_deliver_count_last_month = """select avg(eta * 1.0)  as per_day
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' """

# -- average eta valid and closed trip remark delay in this month
avg_days_deliver_count_this_month = """select avg(eta * 1.0)  as per_day
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' """

# -- total carbon emmision valid and closed trip remark delay in last month till today's date
carbon_emission_count_last_month = """select sum(carbon_emission)  as per_day
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED'"""

# -- total carbon emmision valid and closed trip remark delay in this month
carbon_emission_count_this_month = """select sum(carbon_emission)  as per_day
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
where {where} and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' """

################################################filter data

destination_filter = """select DISTINCT destination
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz order by destination"""
source_filter = """select DISTINCT source from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
order by source"""
date_filter = """select DISTINCT month from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz"""


max_min_date = """select max(file_date) last_updated,min(date(day_and_time_of_dispach)) data_available_from 
from  dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz;"""

#############################################################LEVEL2

l2_open_trips_source_graph = """select open_trip.source, SUM(valid_trip_count) all_valid_trip_count, SUM(open_trip_count) all_open_trip_count ,
        all_open_trip_count*100.0/all_valid_trip_count open_trip_perc
from (select source,sum(open_trip_count) open_trip_count from 
    dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips {where} group by 1) open_trip
inner join (select source,sum(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) valid_trip
on valid_trip.source=open_trip.source
group by open_trip.source
order by all_open_trip_count desc, all_valid_trip_count desc;"""

l2_open_trips_destination_graph = """select open_trip.city_mod, SUM(valid_trip_count) all_valid_trip_count, SUM(open_trip_count) all_open_trip_count ,
        all_open_trip_count*100.0/all_valid_trip_count open_trip_perc
from (select city_mod,sum(open_trip_count) open_trip_count from 
    dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips {where} group by 1) open_trip
inner join (select city_mod,sum(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) valid_trip
on valid_trip.city_mod=open_trip.city_mod
group by open_trip.city_mod
order by all_open_trip_count desc, all_valid_trip_count desc;"""

l2_open_trips_transporter_graph = """select open_trip.transporter_name,
SUM(valid_trip.eta)/sum(valid_trip_count) avg_days_to_deliver,
SUM(valid_trip.distance_covered_kms)/sum(valid_trip_count) avg_distance_covered_kms,
SUM(valid_trip_count) all_valid_trip_count, SUM(open_trip_count) all_open_trip_count ,
all_open_trip_count*100.0/all_valid_trip_count open_trip_perc
from (select transporter_name,sum(open_trip_count), SUM(open_trip_count) open_trip_count,SUM(eta) eta,
    SUM(distance_covered_kms) distance_covered_kms 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips {where}  group by 1) open_trip
inner join (select transporter_name,sum(valid_trip_count) valid_trip_count,SUM(eta) eta,
    SUM(distance_covered_kms) distance_covered_kms 
    from  dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) valid_trip
on valid_trip.transporter_name=open_trip.transporter_name
group by open_trip.transporter_name
order by all_open_trip_count desc, all_valid_trip_count desc;"""

l2_open_trips_calendar = """select open_trip.date_of_dispach, 
valid_trip_count as all_valid_trip_count, open_trip_count as all_open_trip_count,
all_open_trip_count*100.0/all_valid_trip_count open_trip_perc
from (
    select date_of_dispach,SUM(open_trip_count) open_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips {where} group by 1) open_trip
inner join (
    select date_of_dispach,SUM(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) valid_trip 
on valid_trip.date_of_dispach=open_trip.date_of_dispach;"""

l2_open_trips_age_graph = """select open_trip.age_category, 
SUM(valid_trip_count) all_valid_trip_count,
SUM(open_trip_count) open_trip_count 
from (
    select age_category,SUM(open_trip_count) open_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips 
    {where}
    group by 1) open_trip
inner join (
    select age_category,SUM(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips
    {where}
    group by 1) valid_trip 
on  valid_trip.age_category=open_trip.age_category
group by open_trip.age_category;"""


l3_open_trips_other_table = """select distinct row_number() over (order by trip_no) as serial_number, agg.trip_no,
agg.source,agg.city_mod as destination, agg.transporter_name, agg.customer,
CASE 
WHEN  (over_due_days - (google_distance/300)) < 1 THEN 'IN_PROGRESS'
WHEN  (over_due_days - (google_distance/300)) < 2 THEN '1_DAY_LATE'
WHEN (over_due_days - (google_distance/300)) < 16 THEN '1_TO_15_DAY_LATE'
WHEN (over_due_days - (google_distance/300))  < 31 THEN '15_TO_30_DAY_LATE'
WHEN (over_due_days - (google_distance/300))  < 91 THEN '30_TO_90_DAY_LATE'
ELSE '>90_DAY_LATE'
END as age_category,
date(agg.day_and_time_of_dispach) date_of_dispach,
agg.distance_covered_kms,
agg.per_day_km_travelled,
ceiling(google_distance/300) as expected_eta
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'OPEN' {where}
order by serial_number"""


l3_open_trips_in_progress_table = """select distinct row_number() over (order by agg.trip_no) as serial_number,
agg.source,agg.city_mod as destination,agg.trip_no, agg.transporter_name, agg.customer,date(agg.day_and_time_of_dispach) date_of_dispach,
agg.file_date, 
date(agg.day_and_time_of_dispach + ((agg.google_distance/300) * interval '1 day')) as estimated_delivery_date,
(agg.google_distance/300) as target_days_to_deliver, agg.google_distance as distance, agg.distance_covered_kms,
agg.google_distance/(agg.file_date-date(agg.day_and_time_of_dispach)) avg_daily_distance,
(agg.google_distance - agg.distance_covered_kms) / ((agg.google_distance/300)-(agg.file_date-date(agg.day_and_time_of_dispach))) avg_daily_distance_reqd,
pred.pred_probability, pred.predictions
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
inner join (
    select * from dna_hindalco_logistics_transform.prediction_data
    where (trip_no,file_date) in (select trip_no,max(file_date) file_date from dna_hindalco_logistics_transform.prediction_data
    group by 1)) pred 
on pred.trip_no=agg.trip_no
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'OPEN' and (agg.over_due_days - (agg.google_distance/300)) <1 
{where}
order by serial_number;
;"""


l2_destination_filter = """select DISTINCT city_mod
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips open_trip order by city_mod"""
l2_source_filter = """select DISTINCT source from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips open_trip 
order by source"""
l2_date_filter = """select DISTINCT month from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_open_trips open_trip"""

l2_delayed_trips_source = """select source, valid_trip, close_trip, close_delay_trip, round(close_delay_trip*100.0/close_trip) as delay_perc
FROM 
    (select vt.source, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip, 
    sum(close_delay_trip) close_delay_trip
    from (select source, sum(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
    inner join (select source,sum(close_trip_count) close_trip_count  
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips
    {where} group by 1) ct on vt.source=ct.source
    inner join (select source,sum(close_delay_trip_count) close_delay_trip 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_delay_trips
    {where} group by 1) cdt 
    on cdt.source=ct.source
    group by vt.source) as temp
order by delay_perc desc;"""

l2_delayed_trips_destination = """select city_mod, valid_trip, close_trip, close_delay_trip,
round(close_delay_trip*100.0/close_trip) as delay_perc
FROM 
    (select vt.city_mod, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip, 
    sum(close_delay_trip) close_delay_trip
    from (select city_mod, sum(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
    inner join (select city_mod,sum(close_trip_count) close_trip_count  
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips
    {where} group by 1) ct on vt.city_mod=ct.city_mod
    inner join (select city_mod,sum(close_delay_trip_count) close_delay_trip 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_delay_trips
    {where} group by 1) cdt 
    on cdt.city_mod=ct.city_mod
    group by vt.city_mod) as temp
order by delay_perc desc;
"""

l2_delayed_trips_transport = """select transporter_name, valid_trip, close_trip, close_delay_trip, days_to_deliver/valid_trip avg_days_to_deliver,
distance_covered_kms/valid_trip avg_distance_covered,(close_delay_trip*100)/close_trip as delay_perc
FROM
(select vt.transporter_name, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip,
sum(close_delay_trip_count) close_delay_trip, SUM(vt.eta) days_to_deliver,
SUM(vt.distance_covered_kms) distance_covered_kms,
avg(vt.distance_covered_kms * 1.0) as avg_distance_covered
from (select transporter_name,SUM(valid_trip_count) valid_trip_count,SUM(eta) eta,
    SUM(distance_covered_kms) distance_covered_kms 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
    inner join (select transporter_name,SUM(close_trip_count) close_trip_count,SUM(eta) eta,
            SUM(distance_covered_kms) distance_covered_kms 
            from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1) ct  
    on vt.transporter_name=ct.transporter_name
    inner join (select transporter_name,SUM(close_delay_trip_count) close_delay_trip_count,SUM(eta) eta,
            SUM(distance_covered_kms) distance_covered_kms 
            from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_delay_trips {where} group by 1) cdt 
        on  cdt.transporter_name=ct.transporter_name
group by vt.transporter_name)
order by delay_perc desc;"""

l2_delayed_trips_calendar = """select vt.date_of_dispach, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip, 
sum(close_delay_trip_count) close_delay_trip, (close_delay_trip*100)/close_trip as delay_trip_perc
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips vt
left join dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct on vt.source=ct.source
and vt.city_mod=ct.city_mod and vt.transporter_name=ct.transporter_name and vt.date_of_dispach=ct.date_of_dispach
left join dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_delay_trips cdt on cdt.source=ct.source
and cdt.city_mod=ct.city_mod and cdt.transporter_name=ct.transporter_name and cdt.date_of_dispach=ct.date_of_dispach
{where}
group by vt.date_of_dispach"""

l2_delayed_avg_daily_distance_delayed = """select  avg(per_day_km_travelled * 1.0)  as per_day_distance
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
trip_status = 'CLOSED' and delay_category  in ('DELAYED','ONE_DAY_DELAY') 
{where};"""

l2_delayed_avg_daily_distance_non_delayed = """select  avg(per_day_km_travelled * 1.0)  as per_day_distance
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
trip_status = 'CLOSED' and delay_category  in ('EARLY','ONE_DAY_EARLY','ON_TIME') 
{where};"""

l3_delayed_trips_transporter_table = """select distinct row_number()  over(order by main_table.transporter_name) as s_no, 
main_table.transporter_name, 
delayed_avg_daily_distance, 
non_delayed_avg_daily_distance,
closed_trips close_trip,
abs(amount_of_delay) amount_of_delay,
transporter_score,
delay_closed_trips close_delay_trip,
(close_delay_trip*100.0)/close_trip as delay_perc
from (
    select transporter_name, count(distinct trip_no) closed_trips,avg(delay * 1.0) amount_of_delay , 
    avg(final_in_5_score * 1.0) transporter_score
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
    where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
    trip_status = 'CLOSED' 
    {where} group by 1) main_table 
left join
    (select transporter_name, avg(per_day_km_travelled * 1.0) as delayed_avg_daily_distance, count(distinct trip_no) delay_closed_trips
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
    where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
    trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY') 
    {where} group by transporter_name) delayed_table
on delayed_table.transporter_name = main_table.transporter_name
left join
    (select transporter_name, avg(per_day_km_travelled * 1.0) as non_delayed_avg_daily_distance
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
    where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
    trip_status = 'CLOSED' and delay_category in ('EARLY','ONE_DAY_EARLY','ON_TIME')
    {where} group by transporter_name) non_delayed_table
on non_delayed_table.transporter_name = delayed_table.transporter_name
order by transporter_score desc;
"""


l2_delayed_trips_transport_graph = """select vt.transporter_name, sum(close_trip_count) close_trip, 
sum(close_delay_trip_count) close_delay_trip, vt.month,
(close_delay_trip*100)/close_trip as delay_perc
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips vt
left join dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct on vt.source=ct.source
and vt.city_mod=ct.city_mod and vt.transporter_name=ct.transporter_name and vt.date_of_dispach=ct.date_of_dispach
left join dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_delay_trips cdt on cdt.source=ct.source
and cdt.city_mod=ct.city_mod and cdt.transporter_name=ct.transporter_name and cdt.date_of_dispach=ct.date_of_dispach
{where}
group by vt.transporter_name, vt.month
order by vt.month desc"""

l3_delayed_trips_info_table = """select trip_no, source, destination, customer, delay_category, 
CASE WHEN cluster = 'Distance_Cluster' THEN avg(grid_result * 1.0) END as distance_score ,
CASE WHEN cluster = 'Time_Cluster' THEN avg(grid_result * 1.0) END as time_score,
per_day_km_travelled daily_distance, eta days_to_deliver, distance_covered_kms, google_distance
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg 
left join dna_hindalco_logistics_transform.route_similarity_results sr 
on sr.route=(agg.source+'-'+agg.city_mod) and sr.old_shipmentno=agg.trip_no
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
trip_status = 'CLOSED' and delay_category in ('DELAYED','ONE_DAY_DELAY') {where}
group by trip_no, source, destination, customer, delay_category, cluster, per_day_km_travelled, eta, distance_covered_kms,
google_distance;
"""

l3_delayed_trips_fastest_route = """select shipmentno, agg.source, agg.city_mod
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
inner join dna_hindalco_logistics_transform.route_recommendation rr on rr.source=agg.source and rr.destination=agg.city_mod 
and rr.shipmentno=agg.trip_no
where rr.category = 'FASTEST' and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or 
invalid_flag is null) and trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY')
{where};"""

l3_delayed_trips_shortest_route = """select shipmentno, agg.source, agg.city_mod
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
inner join dna_hindalco_logistics_transform.route_recommendation rr on rr.source=agg.source and rr.destination=agg.city_mod 
and rr.shipmentno=agg.trip_no
where rr.category = 'SHORTEST' and (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or 
invalid_flag is null) and trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY')
{where};"""


l3_delayed_trips_greenest_route = """select transporter_name, avg_distance_kms, source, city_mod from 
(select transporter_name, avg(distance_covered_kms * 1.0) avg_distance_kms, source, city_mod
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
    where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
    trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY') {where}
    group by transporter_name, source, city_mod) ft 
order by avg_distance_kms  limit 1;
"""

l3_delayed_trips_best_transporter = """select transporter_name, source, city_mod,avg(final_in_5_score*1.0),count(distinct trip_no)
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz 
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
trip_status = 'CLOSED' and delay_category IN ('DELAYED', 'ONE_DAY_DELAY')
{where}
group by transporter_name, source, city_mod
having count(distinct trip_no) >= 10
order by avg(final_in_5_score*1.0) desc, count(distinct trip_no) desc
limit 1;"""

l2_closed_trips_source = """select vt.source, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip, 
ROUND((close_trip*100.0)/valid_trip) close_trip_perc
from (
    select source,SUM(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
inner join (
    select source,SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1) ct 
on vt.source=ct.source
group by vt.source
order by close_trip_perc;"""

l2_closed_trips_destination = """select vt.city_mod, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip, 
ROUND((close_trip*100.0)/valid_trip) close_trip_perc
from (
    select city_mod,SUM(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
inner join (
    select city_mod,SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1) ct 
on vt.city_mod=ct.city_mod
group by vt.city_mod
order by close_trip_perc;"""

l2_closed_trips_transporter = """select vt.transporter_name, valid_trip_count as valid_trip, close_trip_count as close_trip,  
ROUND((close_trip*100.0)/valid_trip) close_trip_perc,ROUND(eta_sum*1.0/valid_trip) as avg_days_to_deliver,
ROUND(distance_covered_kms*1.0/valid_trip) as avg_distance_covered
from (
    select transporter_name,SUM(valid_trip_count) valid_trip_count,SUM(eta) eta_sum,
    SUM(distance_covered_kms) distance_covered_kms 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
inner join (
    select transporter_name,SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1) ct 
on vt.transporter_name=ct.transporter_name
order by close_trip_perc;"""

# l2_closed_trips_day_to_deliver = """select ct.days_to_deliver_category,valid_trip,close_trip,(close_trip*100.0)/valid_trip as close_trip_perc
# from (
#     select
#     CASE
#     WHEN eta  <= 0 THEN  '0'
#     WHEN  eta<1 THEN  '0-1'
#     WHEN  eta<2 THEN  '1-2'
#     WHEN  eta<3 THEN  '2-3'
#     WHEN  eta<4 THEN  '3-4'
#     WHEN  eta<5 THEN  '4-5'
#     WHEN  eta<6 THEN  '5-6'
#     WHEN  eta<7 THEN  '6-7'
#     WHEN  eta<8 THEN  '7-8'
#     ELSE '> 8'
#     END as days_to_deliver_category,
#     count(distinct trip_no) valid_trip from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
#     where  (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)
#     {where} group by 1) vt
# inner join (
#     select
#     CASE
#     WHEN eta  <= 0 THEN  '0'
#     WHEN eta<1 THEN  '0-1'
#     WHEN eta<2 THEN  '1-2'
#     WHEN eta<3 THEN  '2-3'
#     WHEN eta<4 THEN  '3-4'
#     WHEN eta<5 THEN  '4-5'
#     WHEN eta<6 THEN  '5-6'
#     WHEN eta<7 THEN  '6-7'
#     WHEN eta<8 THEN  '7-8'
#     ELSE '> 8'
#     END as days_to_deliver_category,
#     count(distinct trip_no) close_trip from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
#     where  (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)
#     and trip_status = 'CLOSED' {where} group by 1) ct
# on  vt.days_to_deliver_category=ct.days_to_deliver_category;
# """

l2_closed_trips_day_to_deliver = """select ct.days_to_deliver_category,valid_trip,close_trip,(close_trip*100.0)/valid_trip as close_trip_perc
from (
    select 
    count(distinct trip_no) valid_trip from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
    where  (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)
    {where} 
    ) vt
 cross join (
    select 
    CASE
    WHEN eta  <= 0 THEN  '0'
    WHEN eta<1 THEN  '0-1'
    WHEN eta<2 THEN  '1-2'
    WHEN eta<3 THEN  '2-3'
    WHEN eta<4 THEN  '3-4'
    WHEN eta<5 THEN  '4-5'
    WHEN eta<6 THEN  '5-6'
    WHEN eta<7 THEN  '6-7'
    WHEN eta<8 THEN  '7-8'
    ELSE '> 8'
    END as days_to_deliver_category,
    count(distinct trip_no) close_trip from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
    where  (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
    and trip_status = 'CLOSED'
    {where} 
    group by 1) ct;
"""

l2_closed_trips_calendar = """select vt.date_of_dispach, valid_trip_count as valid_trip, close_trip_count as close_trip, 
(close_trip*100)/valid_trip as close_trip_perc
from (
    select  date_of_dispach, SUM(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips {where} group by 1) vt
inner join (
    select  date_of_dispach, SUM(close_trip_count) close_trip_count from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips
    {where} group by 1) ct 
on vt.date_of_dispach=ct.date_of_dispach;"""

l2_closed_trips_transporter_graph = """select vt.transporter_name, sum(valid_trip_count) valid_trip, sum(close_trip_count) close_trip, 
vt.month,
(close_trip*100)/valid_trip as close_perc
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips vt
left join dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct on vt.source=ct.source
and vt.city_mod=ct.city_mod and vt.transporter_name=ct.transporter_name and vt.date_of_dispach=ct.date_of_dispach
{where}
group by vt.transporter_name, vt.month
order by vt.month desc"""

l3_closed_trips_info = """select
trip_no, source, city_mod, transporter_name, customer, date(day_and_time_of_dispach) dispatch_date,
delay_category, round(distance_covered_kms) as distance_covered, round(per_day_km_travelled) as per_day_km_travelled, eta,
date(agg.day_and_time_of_dispach + (eta * interval '1 day')) as estimated_delivery_date
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) 
and trip_status = 'CLOSED' 
{where}
order by trip_no
{limit}
{offset};"""


l2_forceful_closure_trips_source = """select ct.source, close_trip_count as close_trip, 
close_forcefull_trip as close_forcefull_trip,ROUND((close_forcefull_trip*100.0)/close_trip) as forcefull_perc
from (
    select source, SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips group by 1) ct
inner join (
    select source, SUM(close_delay_trip_count) close_forcefull_trip 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_forcefull_closure_trips {where}  group by 1) cdt 
on cdt.source=ct.source
order by forcefull_perc desc;"""


l2_forceful_closure_trips_destination = """select ct.city_mod, close_trip_count as close_trip, 
close_forcefull_trip as close_forcefull_trip,ROUND((close_forcefull_trip*100.0)/close_trip) as forcefull_perc
from (
    select city_mod, SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips  group by 1) ct
inner join (
    select city_mod, SUM(close_delay_trip_count) close_forcefull_trip 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_forcefull_closure_trips {where} group by 1) cdt on 
cdt.city_mod=ct.city_mod
order by forcefull_perc desc;
"""

# l2_forceful_closure_trips_customer = """select ct.customer_name, close_trip_count as close_trip,
# close_forcefull_trip as close_forcefull_trip,ROUND((close_forcefull_trip*100.0)/close_trip) as forcefull_perc
# from (
#     select customer as customer_name, count( distinct trip_no) close_trip_count
#     from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
#     where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)
#     and trip_status = 'CLOSED' group by 1) ct
# inner join (
#     select customer_name, SUM(close_delay_trip_count) close_forcefull_trip
#     from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_forcefull_closure_trips {where} group by 1) cdt
# on cdt.customer_name=ct.customer_name
# order by forcefull_perc desc;
# """

l2_forceful_closure_trips_customer = """select ct.customer_name, close_trip_count as close_trip,
close_forcefull_trip as close_forcefull_trip,ROUND((close_forcefull_trip*100.0)/close_trip) as forcefull_perc,transporter_name,close_forcefull_trip_trans
from (
    select customer as customer_name, count( distinct trip_no) close_trip_count
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz
    where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)
    and trip_status = 'CLOSED' group by 1) ct
inner join (
    select customer_name, SUM(close_delay_trip_count) close_forcefull_trip
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_forcefull_closure_trips
    {where}
    group by 1) cdt
on cdt.customer_name=ct.customer_name
inner join (
    select customer_name,transporter_name, SUM(close_delay_trip_count) close_forcefull_trip_trans
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_forcefull_closure_trips
    {where}
    group by 1,2) cdt_trans
on cdt_trans.customer_name=ct.customer_name
order by forcefull_perc desc;
"""

l2_forceful_closure_trips_calendar = """select vt.date_of_dispach, valid_trip_count as valid_trip, 
close_trip_count as close_trip, close_delay_trip_count as forcefull_delay_trip, 
ROUND((forcefull_delay_trip*100.0)/close_trip) as forcefull_trip_perc
from (
    select date_of_dispach,SUM(valid_trip_count) valid_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_valid_trips group by 1) vt
inner join (
    select date_of_dispach,SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips group by 1) ct 
on  vt.date_of_dispach=ct.date_of_dispach
left join (
    select date_of_dispach,SUM(close_delay_trip_count) close_delay_trip_count from 
    dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_forcefull_closure_trips {where} group by 1) cdt 
on  cdt.date_of_dispach=ct.date_of_dispach"""


l3_forceful_closure_trips_info = """select
trip_no, source, city_mod, transporter_name, customer, date(day_and_time_of_dispach) dispatch_date,
delay_category, ROUND(distance_covered_kms) as distance_covered, ROUND(per_day_km_travelled) as per_day_km_travelled, eta,
date(agg.day_and_time_of_dispach + (eta * interval '1 day')) as estimated_delivery_date
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and 
trip_status = 'CLOSED' and (closer_remarks = 'forcefull_closure' OR closer_remarks is null)
{where}
order by trip_no
{limit}
{offset}
;
"""

l2_days_to_deliver_source = """select source, eta/close_trip avg_days_deliver, close_trip 
from (
    select ct.source, sum(eta) as eta, SUM(close_trip_count) close_trip
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct
    {where}
    group by 1)
order by avg_days_deliver desc;"""

l2_days_to_deliver_destination = """select ct.city_mod, eta/close_trip_count as avg_days_deliver,distance_covered_kms,
distance_covered_kms/close_trip_count as avg_distance_covered_kms, close_trip_count close_trip
from (
    select city_mod,SUM(close_trip_count) close_trip_count,sum(eta) eta,SUM(distance_covered_kms) distance_covered_kms
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1) ct 
order by avg_days_deliver desc;"""


l2_days_to_deliver_transporter = """select ct.transporter_name, ct.eta/close_trip_count as avg_days_deliver, 
ct.distance_covered_kms/close_trip_count as avg_daily_distance, close_trip_count as close_trip
from (
    select transporter_name,SUM(eta) eta,SUM(distance_covered_kms) distance_covered_kms,
    SUM(close_trip_count) close_trip_count 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1) ct
order by avg_days_deliver desc;"""

l2_days_to_deliver_transporter_graph = """select ct.transporter_name, ct.eta/close_trip_count as avg_days_deliver,
ct.month
from (
    select transporter_name as transporter_name, month,sum(eta) eta,SUM(close_trip_count) close_trip_count
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips
    {where}
    group by 1,2) ct 

order by ct.month desc;"""

l2_days_to_deliver_avg = """select 
CASE
WHEN ct.eta  = 0 THEN  '0'
WHEN ct.eta > 0 and ct.eta<1 THEN  '0-1'
WHEN ct.eta >= 1 and ct.eta<2 THEN  '1-2'
WHEN ct.eta >= 2 and ct.eta<3 THEN  '2-3'
WHEN ct.eta >= 3 and ct.eta<4 THEN  '3-4'
WHEN ct.eta >= 4 and ct.eta<5 THEN  '4-5'
WHEN ct.eta >= 5 and ct.eta<6 THEN  '5-6'
WHEN ct.eta >= 6 and ct.eta<7 THEN  '6-7'
WHEN ct.eta >= 7 and ct.eta<8 THEN  '7-8'
ELSE '> 8'
END as days_to_deliver_category,
CASE
WHEN delay_category = 'EARLY' or delay_category = 'ONE_DAY_EARLY' THEN 'early'
WHEN delay_category= 'ONE_DAY_DELAY' or delay_category = 'DELAYED' THEN 'delayed'
ELSE 'on_time'
END as delay_group,
sum(close_trip_count) close_trip
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct 
{where}
group by days_to_deliver_category, delay_group;"""


l2_days_to_deliver_calendar = """select ct.date_of_dispach, 
close_trip_count as close_trip, ct.eta/close_trip_count as avg_days_deliver
from (
    select date_of_dispach, sum(close_trip_count) close_trip_count,sum(eta) eta 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1 ) ct
;"""

l3_days_to_deliver_info = """select
trip_no, source, city_mod, transporter_name, customer, date(day_and_time_of_dispach) dispatch_date,
delay_category, (distance_covered_kms * 1.0) distance_covered, per_day_km_travelled, eta,
date(agg.day_and_time_of_dispach + ((agg.google_distance/300) * interval '1 day')) as estimated_delivery_date,
CASE
WHEN delay_category = 'EARLY' or delay_category = 'ONE_DAY_EARLY' THEN 'EARLY'
WHEN delay_category= 'ONE_DAY_DELAY' or delay_category = 'DELAYED' THEN 'DELAYED'
ELSE 'ON TIME'
END as delay_group
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null)
and trip_status = 'CLOSED'
{where}
order by trip_no
{limit}
{offset}
;
"""

l2_daily_distance_source = """select source,close_trip,distance_covered_kms/close_trip as avg_daily_distance
from (
    select ct.source, sum(close_trip_count) close_trip, sum(ct.distance_covered_kms) distance_covered_kms
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct 
    {where} group by 1)
order by avg_daily_distance desc;"""

l2_daily_distance_destination = """select city_mod,close_trip,distance_covered_kms/close_trip as avg_daily_distance
from ( 
    select ct.city_mod, sum(close_trip_count) close_trip, sum(ct.distance_covered_kms) distance_covered_kms
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct 
    {where} group by 1)
order by avg_daily_distance desc;
"""

l2_daily_distance_transporter = """select transporter_name,close_trip,distance_covered_kms/close_trip as avg_daily_distance, 
eta/close_trip as  avg_days_deliver
from ( 
    select ct.transporter_name, sum(close_trip_count) close_trip, sum(ct.distance_covered_kms) distance_covered_kms, 
    SUM(eta) eta
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct 
    {where} group by 1)
order by avg_daily_distance desc;"""

l2_daily_distance_transporter_graph = """select ct.transporter_name, ct.distance_covered_kms/close_trip_count as avg_daily_distance,ct.month
from (
    select transporter_name as transporter_name, month,sum(distance_covered_kms) distance_covered_kms,SUM(close_trip_count) close_trip_count
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips
    {where} group by 1,2) ct 
order by ct.month desc;"""

l2_daily_distance_calendar = """select ct.date_of_dispach, 
close_trip_count as close_trip, ct.distance_covered_kms/close_trip_count as avg_daily_distance
from ( 
    select date_of_dispach, sum(close_trip_count) close_trip_count,sum(distance_covered_kms) distance_covered_kms 
    from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips {where} group by 1 ) ct
;"""

l2_daily_distance_avg = """select
CASE
WHEN ct.distance_covered_kms = 0 THEN '0'
WHEN ct.distance_covered_kms <= 50 THEN '0-50'
WHEN ct.distance_covered_kms <= 100 THEN '50-100'
WHEN ct.distance_covered_kms <= 150 THEN '100-150'
WHEN ct.distance_covered_kms <= 200 THEN '150-200'
WHEN ct.distance_covered_kms <= 250 THEN '200-250'
WHEN ct.distance_covered_kms <= 300 THEN '250-300'
else '>300'
END as distance_covered_kms_category,
 sum(close_trip_count) close_trip
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_close_trips ct 
{where}
group by distance_covered_kms_category;"""

l3_daily_distance_info = """select
trip_no, source, city_mod, transporter_name, customer, date(day_and_time_of_dispach) dispatch_date,
(distance_covered_kms * 1.0) distance_covered, per_day_km_travelled, eta,
date(agg.day_and_time_of_dispach + ((agg.google_distance/300) * interval '1 day')) as estimated_delivery_date,
CASE
WHEN delay_category = 'EARLY' or delay_category = 'ONE_DAY_EARLY' THEN 'EARLY'
WHEN delay_category= 'ONE_DAY_DELAY' or delay_category = 'DELAYED' THEN 'DELAYED'
ELSE 'ON TIME'
END as delay_group
from dna_hindalco_logistics_analytics.daily_report_plant_trip_agg_viz agg
where (invalid_flag in ('TRANSIT_HOURS_IS_HIGHER','TRANSIT_HOURS_IS_NOT_CORRECT') or invalid_flag is null) and
trip_status = 'CLOSED'
{where}
order by trip_no
{limit}
{offset}
;
"""
