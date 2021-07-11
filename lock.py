#!/usr/bin/env python3
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

from sthope_env import *
from tuya_iot import *

DOORLOCK_TOPIC = "TYAPI/doorlock"
DOORLOCK_TOPIC_CMD = "TYAPI/doorlock/cmd"
DOORLOCK_TOPIC_STATUS = "TYAPI/doorlock/status"

def on_connect(client, userdata, flags, rc):
    client.subscribe(DOORLOCK_TOPIC + "/+")
    # client.subscribe("TYAPI")
 
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.payload == str("get_token"):
        xyz = openapi.get('/v1.0/token?grant_type=1')
        client.publish(DOORLOCK_TOPIC_STATUS, json.dumps(xyz))

    if msg.payload == "test2":
        print("Received message #2, do something else")

## Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.login(USERNAME, PASSWORD, COUNTRY_CODE, SCHEMA)

# Create an MQTT client and attach our routines to it.
client = mqtt.Client(MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_forever()