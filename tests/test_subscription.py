import time
import pytest
from  mqtt_client import mqtt_client
import ssl

from config import conf

@pytest.fixture
def get_mqtt_client():
    """Returns a mqtt client bases on conf.py settings"""
    sslcontext = None
    if conf.get('ssl'):
        sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        sslcontext.load_cert_chain(
            certfile=conf.get('certfile', ''),
            keyfile=conf.get('keyfile'),
            password=conf.get('password'),
        )
    # (password=XXX) givs pw for keyfiles. Key can be in the CA file, but first.

    mc = mqtt_client.Mqtt_Client("mqtt_tree")
    mc.configure(conf.get('mqtt_server'), conf.get('mqtt_port'), sslcontext=sslcontext)
    mc.run()
    return mc

def test_subscribe(get_mqtt_client: mqtt_client.Mqtt_Client):
    test_topic = "Notifier/#"
    test_topic = "XXXXXNotifier/+/wurst/+"
    get_mqtt_client.subscribe(test_topic)
    # while True:
    #     pass
    time.sleep(0.5)
    subscript_attr = mqtt_client.SubscriptionAtrributes(test_topic)
    assert subscript_attr in get_mqtt_client.topics

def test_publish(get_mqtt_client: mqtt_client.Mqtt_Client):
    test_topic = "Notifier/test"
    payload = "Some Thing"
    response = b""
    def __cb_on_message(mqttc, obj, msg):
        nonlocal response
        response = msg.payload
    get_mqtt_client.on_message = __cb_on_message    
    get_mqtt_client.subscribe(test_topic)
    get_mqtt_client.publish(test_topic, payload=payload)
    time.sleep(1)
    assert payload == response.decode()
