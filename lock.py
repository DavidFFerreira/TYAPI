#!/usr/bin/env python3
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

from sthope_env import *
from tuya_iot import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 16

DOORLOCK_TOPIC = "TYAPI/doorlock"
DOORLOCK_TOPIC_CMD = "TYAPI/doorlock/cmd"
DOORLOCK_TOPIC_STATUS = "TYAPI/doorlock/status"

def on_connect(client, userdata, flags, rc):
    client.subscribe(DOORLOCK_TOPIC + "/#")
    # client.subscribe("TYAPI")

def on_message(client, userdata, msg):

  if msg.topic == DOORLOCK_TOPIC_CMD and msg.payload.decode() == "get_token":
      xyz = openapi.get('/v1.0/token?grant_type=1')
      client.publish(DOORLOCK_TOPIC_STATUS, json.dumps(xyz))

  if msg.topic == DOORLOCK_TOPIC_CMD and msg.payload.decode() == "parse_password_ticket":
      x = json.dumps(openapi.post('/v1.0/devices/' + DEVICE_ID + '/door-lock/password-ticket'))
      y = json.loads(x)
      PasswordTicket = y["result"]["ticket_key"]
      lock_pincode = print(pad(str.encode(LOCKPINCODE), BLOCK_SIZE))
      cipher = AES.new(decrypted_msg.encode('utf8'), AES.MODE_ECB)
      msg = cipher.encrypt(lock_pincode)
      l = msg.hex()
      client.publish(DOORLOCK_TOPIC_STATUS, json.dumps(l))

  if msg.topic == DOORLOCK_TOPIC_CMD and msg.payload.decode() == "unlock_door":
      xyz = openapi.post('/v1.0/devices/' + DEVICE_ID + '/door-lock/open-door', {
          'password_type': 'ticket',
          'password': "",
          'ticket_id': '',
          })
      client.publish(DOORLOCK_TOPIC_STATUS, json.dumps(xyz))

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