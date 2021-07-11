#!/usr/bin/env python3

import json
import logging

from Crypto.Util import Padding
from tuya_iot import *
from sthope_env import *

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 16

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