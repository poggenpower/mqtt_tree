#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# All rights reserved.

# This shows a simple example of an MQTT subscriber using a per-subscription message handler.

import paho.mqtt.client as mqtt
from queue import Queue
import logging
logger = logging.getLogger(__name__)

class Mqtt_Client(mqtt.Client):

    _queue = Queue()

    def on_connect(self, mqttc, obj, flags, rc):
        logger.info("rc: "+str(rc))

    def on_disconnect(self, userdata, rc):
        if rc != 0:
            logger.error("Mqtt_Client: Disconnected unexpected.")
            try:
                self.reconnect()
            except TimeoutError as te:
                logger.exception("Mqtt_Client: Reconnect failed.")

    def on_message(self, mqttc, obj, msg):
        #logger.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        self._queue.put(msg)

    def on_publish(self, mqttc, obj, mid):
        logger.info("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.info("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        # logger.info("Log: " + string)
        pass

    def get_queue(self):
        return self._queue

    def run(self, *topics):
        self.connect("haus.wupp", 1883, 60)
        for topic in topics:
            self.subscribe(topic, 0)
        self.loop_start()
