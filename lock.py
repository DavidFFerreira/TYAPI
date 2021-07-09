#!/usr/bin/env python3

import json
import logging
from Crypto.Util import Padding
from tuya_iot import *
from env import *
import random
import time
import paho.mqtt.client as mqtt
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 16

## Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, ProjectType.SMART_HOME)
openapi.login(USERNAME, PASSWORD, COUNTRY_CODE, SCHEMA)

## Turn on Debug
# tuya_logger.setLevel(logging.DEBUG)

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

##### Unlock Lock
# openapi.post('/v1.0/devices/' + DEVICE_ID + '/door-lock/open-door', {
#     'password_type': 'ticket',
#     'password': "",
#     'ticket_id': '',
# })
