#!/usr/bin/env python3
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

from sthope_env import *
from tuya_iot import *

from Crypto.Cipher import AES

## Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, ProjectType.SMART_HOME)
openapi.login(USERNAME, PASSWORD, COUNTRY_CODE, SCHEMA)

x = openapi.get('/v1.0/scales/' + WIFI_SCALE + '/datas/history?device_id=' + WIFI_SCALE + '&page_no=' + PAGE_NO + '&page_size=' + PAGE_SIZE + '&user_id=' + SCALE_USER_ID)
y = json.dumps(x)
z = json.loads(y)
xyz = z["result"]["records"]
# client.publish(WIFI_SCALE_TOPIC + "/status", xyz))
print(xyz)

