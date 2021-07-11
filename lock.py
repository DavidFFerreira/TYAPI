#!/usr/bin/env python3

import json
import logging
from Crypto.Util import Padding
from tuya_iot import *
from sthope_envs import *
import paho.mqtt.client as mqtt
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 16

## Connect to MQTT Broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

## Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.login(USERNAME, PASSWORD, COUNTRY_CODE, SCHEMA)

## Turn on Debug
#tuya_logger.setLevel(logging.DEBUG)

## Get Access_token
def get_access_token():
    x = openapi.get('/v1.0/token?grant_type=1')
    print(x)

## Parse TuyaLock Password-Ticket:
def parse_password_ticket():
    x = json.dumps(openapi.post('/v1.0/devices/' + DEVICE_ID + '/door-lock/password-ticket'))
    y = json.loads(x)
    PasswordTicket = y["result"]["ticket_key"]
    lock_pincode = pad(b'123456', BLOCK_SIZE)
    cipher = AES.new(decrypted_msg.encode('utf8'), AES.MODE_ECB)
    msg = cipher.encrypt(lock_pincode)
    l = msg.hex()
    #print(l)

def unlock_doorlock():
    x = openapi.post('/v1.0/devices/' + DEVICE_ID + '/door-lock/open-door', {
        'password_type': 'ticket',
        'password': "",
        'ticket_id': '',
        })
    print(x)

def get_mqtt_access():
    h = openapi.post('/v1.0/open-hub/access/config', {
        'uid': ACCESS_ID,
        'link_id': 'test',
        'link_type': 'mqtt',
        'topics': 'device',
        })

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(MQTT_TOPIC)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()