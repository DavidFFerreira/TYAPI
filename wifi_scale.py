#!/usr/bin/env python3
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

from sthope_env import *
from tuya_iot import *

def on_connect(client, userdata, flags, rc):
    client.subscribe(WIFI_SCALE_TOPIC + "/#")
    client.publish(WIFI_SCALE_TOPIC_LWT, "Online")
    if HA_DISCOVERY == "true":
        client.publish(HA_DISCOVERY_TOPIC, HA_DISCOVERY_MSG, qos=0, retain=True )

def on_message(client, userdata, msg):

  if msg.topic == WIFI_SCALE_TOPIC_CMD and msg.payload.decode() == "sthope_records":
      x = openapi.get('/v1.0/scales/' + WIFI_SCALE + '/datas/history?device_id=' + WIFI_SCALE + '&page_no=' + PAGE_NO + '&page_size=' + PAGE_SIZE + '&user_id=' + SCALE_USER_ID)
      y = json.dumps(x)
      client.publish(WIFI_SCALE_TOPIC_STATUS, y)

  if msg.topic == WIFI_SCALE_TOPIC_CMD and msg.payload.decode() == "list_users":
      x = openapi.get('/v1.0/devices/' + WIFI_SCALE + '/users')
      xyz = json.dumps(x)
      client.publish(WIFI_SCALE_TOPIC_STATUS, xyz)

  if msg.topic == WIFI_SCALE_TOPIC_CMD and msg.payload.decode() == "all_records":
      x = openapi.get('/v1.0/scales/' + WIFI_SCALE + '/datas/history?device_id=' + WIFI_SCALE + '&page_no=' + PAGE_NO + '&page_size=' + PAGE_SIZE)
      y = json.dumps(x)
      z = json.loads(y)
      xyz = (z['result']['records'])
      client.publish(WIFI_SCALE_TOPIC_STATUS, y)

  if msg.topic == WIFI_SCALE_TOPIC_CMD and msg.payload.decode() == "fake_report":
      x = openapi.post('/v1.0/scales/' + WIFI_SCALE + '/analysis-reports', {
          'height': FAKE_HEIGHT,
          'weight': FAKE_WEIGHT,
          'age': FAKE_AGE,
          'sex': FAKE_SEX,
          'resistance': FAKE_RESISTANCE,
          })
      y = json.dumps(x)
      z = json.loads(y)
      client.publish(WIFI_SCALE_TOPIC_STATUS, z)

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, ProjectType.SMART_HOME)
openapi.login(USERNAME, PASSWORD, COUNTRY_CODE, SCHEMA)

client = mqtt.Client(MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEP_ALIE_INTERVAL)

client.loop_forever()