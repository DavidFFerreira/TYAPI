#!/usr/bin/env python3

import logging
from tuya_iot import *
from sthope_env import *
from env import *
import json

PAGE_NO = '1'
PAGE_SIZE = '999'
FAKE_HEIGHT = '180'
FAKE_WEIGHT = '666'
FAKE_AGE = '35'
FAKE_SEX = '1'
FAKE_RESISTANCE = '683'
SCALE_USER_ID = '0000003qk0'

# Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, ProjectType.SMART_HOME)
openapi.login(USERNAME, PASSWORD, COUNTRY_CODE, SCHEMA)

# Turn ON Debug Log
#tuya_logger.setLevel(logging.DEBUG)

def get_scale_records():
    x = openapi.get('/v1.0/scales/' + WIFI_SCALE + '/datas/history?device_id=' + WIFI_SCALE + '&page_no=' + PAGE_NO + '&page_size=' + PAGE_SIZE + '&user_id=' + SCALE_USER_ID)
    y = json.dumps(x)
    z = json.loads(y)
    print(z["result"]["records"])

def get_all_scale_records():
    x = openapi.get('/v1.0/scales/' + WIFI_SCALE + '/datas/history?device_id=' + WIFI_SCALE + '&page_no=' + PAGE_NO + '&page_size=' + PAGE_SIZE)
    y = json.dumps(x)
    z = json.loads(y)
    print(z["result"]["records"])

def create_fake_report():
    x = openapi.post('/v1.0/scales/' + WIFI_SCALE + '/analysis-reports', {
        'height': FAKE_HEIGHT,
        'weight': FAKE_WEIGHT,
        'age': FAKE_AGE,
        'sex': FAKE_SEX,
        'resistance': FAKE_RESISTANCE,})
    y = json.dumps(x)
    z = json.loads(y)
    print(z)

get_scale_records()