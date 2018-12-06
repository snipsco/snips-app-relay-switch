#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import time
import sys
from threading import Thread
import RPi.GPIO as GPIO

CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class RelaySwitch(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            print 'No "config.ini" found!'
            sys.exit(1)

        self.relay_pin = int(self.config.get('global',{"gpio_bcm_relay":"12"}).get('gpio_bcm_relay','12'))

        if self.config.get('global',{"activate_level":"high"}).get('activate_level','high') == 'high':
            self.relay_on = GPIO.HIGH
            self.relay_off = GPIO.LOW
        elif self.config.get('global',{"activate_level":"high"}).get('activate_level','high') == 'low':
            self.relay_on = GPIO.HIGH
            self.relay_off = GPIO.LOW

        self.snips_user = str(self.config.get('global',{"snips_user_name":""}).get('snips_user_name',''))
        if self.snips_user is not '':
            self.snips_user += ':'

        self.site_id = str(self.config.get('secret',{"site_id":"default"}).get('site_id','default'))
        self.site_id = str(self.config.get('secret',{"device_name":"default"}).get('device_name','default'))
        self.gpioInit()
        self.start_blocking()

    # -> hardware related
    def gpioInit(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin, GPIO.OUT)
        GPIO.output(self.relay_pin, self.relay_off)

    # -> extraction of slots value
    def extractHouseRoom(self, intent_message, default_value):
        #if intent_message.slots.house_room:
        #    return intent_message.slots.house_room.first()
        return default_value

    def extractDevice(self, intent_message, default_value):
        #if intent_message.slots.device:
        #    return intent_message.slots.device.first()
        return default_value

    # -> action callbacks
    def turnOnRelay(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        GPIO.output(self.relay_pin, self.relay_on)
        hermes.publish_end_session(intent_message.session_id, "")

    def turnOffRelay(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        GPIO.output(self.relay_pin, self.relay_off)
        hermes.publish_end_session(intent_message.session_id, "")

    def master_intent_callback(self, hermes, intent_message):
        if self.site_id != intent_message.site_id:
            print "[Return] Site Id unmatch"
            return

        if intent_message.intent.intent_name == 'relayTurnOn':
            self.turnOnRelay(hermes, intent_message)
        if intent_message.intent.intent_name == 'relayTurnOff':
            self.turnOffRelay(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    RelaySwitch()
