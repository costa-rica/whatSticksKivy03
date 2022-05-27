import json;import datetime;from datetime import timedelta;import os, zipfile;
import requests
import time
import pytz
from pytz import timezone

base_url = 'https://api.what-sticks-health.com'
# base_url = 'http://localhost:8000'

def add_activity_util(title, note,user_id,user_timezone,datetime_thing, user_email,login_token):
    url=base_url + "/add_activity"
    print('**** Add activity ****')
    payload={}
    #convert datetime_thing to string
    datetime_thing_str=datetime_thing.strftime('%Y-%m-%dT%H:%M:%S')
    # payload['datetime_of_activity']=datetime_thing_str
    # payload["note"]= note
    # payload["source_name"]= "phone application"
    # payload["time_stamp_utc"]= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    # payload["user_id"]= user_id
    # payload["var_activity"]= title
    user_tz = timezone(user_timezone)
    datetime_tz_aware=user_tz.localize(datetime_thing)
    timezone_delta=datetime_tz_aware.utcoffset().total_seconds()/60
    # payload["var_timezone_utc_delta_in_mins"]= timezone_delta
    # payload['time_offset']=timezone_delta
    # payload["var_type"]= "Activity"


    payload = {
                'datetime_of_activity':datetime_thing_str,
                'time_offset': timezone_delta,
                'var_activity':title,
                'user_id':user_id,
                'source_name': 'iphone',
                # 'source_notes':'no notes',
                'weight': 150,
                'note': note
                }

    headers={'Content-Type':'application/json','x-access-token':login_token}
    # headers['Content-Type']='application/json'
    # headers['x-access-token'] = login_token

    response = requests.request("POST", url, headers=headers,
        data=str(json.dumps(payload)))
    print('api response:::',response.status_code)
    # return ('success! ', payload)

def current_time_util(user_timezone):
    date_time_obj=datetime.datetime.now()
    date_time_obj_tz_aware=timezone(user_timezone).localize(date_time_obj)
    hour_temp=date_time_obj_tz_aware.strftime("%H")
    hour=hour_temp if hour_temp[0]!='0' else hour_temp[1]

    am_pm='AM' if int(hour)<12 else 'PM'

    hour=hour if int(hour)<13 else str(int(hour)-12)
    minute=date_time_obj_tz_aware.strftime("%M")
    # time_thing=date_time_obj_tz_aware.strftime("%H:%M%p")
    time_thing=f'{hour}:{minute} {am_pm}'
    date_thing=date_time_obj_tz_aware.strftime("%m/%d/%Y")

    date_time_now=(date_thing,time_thing)

    return(date_time_now)


def log_activity_util(datetime_thing,title, note,user_id,timezone_delta):
    payload={}
