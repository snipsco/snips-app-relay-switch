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

SNIPS_USER = ''

GOOD_THRESHOLD = 0.4
BAD_THRESHOLD = 0.2

COEFFICIENT = 10

class RelaySwitch(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            print 'No "config.ini" found!'
            sys.exit(1)

        self.relay_pin = int(self.config.get('secret',{"gpio_bcm_relay":"12"}).get('gpio_bcm_relay','12'))

        if self.config.get('secret',{"activate_level":"high"}).get('activate_level','high') == 'high':
            self.relay_on = GPIO.HIGH
            self.relay_off = GPIO.LOW
        elif self.config.get('secret',{"activate_level":"high"}).get('activate_level','high') == 'low':
            self.relay_on = GPIO.HIGH
            self.relay_off = GPIO.LOW

        self.site_id = self.config.get('secret',{"site_id":"living room"}).get('site_id','living room')
        self.gpioInit()
        self.move_to_percentage(100)
        self.start_blocking()
        
    # -> hardware related
    def gpioInit(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin, GPIO.OUT)
        GPIO.output(self.relay_pin, self.relay_off)

    # -> extraction of slots value
    def extractHouseRoom(self, intent_message, default_value):
        pass
        return house_room

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
        if intent_message.intent.probability < BAD_THRESHOLD:
            return
        elif intent_message.intent.probability <= GOOD_THRESHOLD:
            hermes.publish_end_session(intent_message.session_id, "Sorry, I dont think I understood")
            return
        if self.extractHouseRoom(intent_message, self.site_id) != intent_message.site_id:
            return

        if intent_message.intent.intent_name == '{}turnOnRelay'.format(SNIPS_USER):
            self.turnOnRelay(hermes, intent_message)
        if intent_message.intent.intent_name == '{}turnOffRelay'.format(SNIPS_USER):
            self.turnOffRelay(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    RelaySwitch()
