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

    def configure(self, hostname, port, timeout=60, sslcontext=None):
        """ create an ssl context like this:
        import ssl
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="../code2/codeschloss.home.schmu.net.crt", keyfile="../code2/codeschloss.home.schmu.net.key.pem")
        (password=XXX) givs pw for keyfiles. Key can be in the CA file, but first.
        """
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.sslcontext = sslcontext

    def on_connect(self, mqttc, obj, flags, rc):
        for topic in self.topics:
            self.subscribe(topic, 0)
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
        if not self.hostname:
            raise AttributeError("Hostname and Port need to be configurted. all .configure()")
        if self.sslcontext:
            self.tls_set_context(self.sslcontext)
        self.connect(self.hostname, self.port, self.timeout)
        self.topics = topics
        self.loop_start()
