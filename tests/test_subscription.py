import time
import pytest
import sys
import random
from mqtt_client import mqtt_client
import ssl

from config import conf


@pytest.fixture
def get_mqtt_client(will_send_online=False):
    """Returns a mqtt client bases on conf.py settings"""
    sslcontext = None
    if conf.get("ssl"):
        sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        sslcontext.load_cert_chain(
            certfile=conf.get("certfile", ""),
            keyfile=conf.get("keyfile"),
            password=conf.get("password"),
        )
    # (password=XXX) givs pw for keyfiles. Key can be in the CA file, but first.
    rnd_suffix = "".join((random.choice("abcdef1234567890") for i in range(5)))
    mc = mqtt_client.Mqtt_Client("mqtt_tree_pytest" + rnd_suffix)
    mc.configure(conf.get("mqtt_server"), conf.get("mqtt_port"), sslcontext=sslcontext)
    mc.will_set("Notifier.lwt", payload="Offline", retain=False)
    mc.will_send_online = will_send_online
    mc.run()
    print("Wait for connection ", end="")
    while not mc.connected:
        print(".", end="")
        time.sleep(1)
    print("")
    return mc


def test_subscribe(get_mqtt_client: mqtt_client.Mqtt_Client):
    test_topic = "Notifier/#"
    test_topic = "XXXXXNotifier/+/wurst/+"
    get_mqtt_client.subscribe(test_topic)
    # while True:
    #     pass
    time.sleep(0.5)
    subscript_attr = mqtt_client.SubscriptionAttributes(test_topic)
    assert subscript_attr in get_mqtt_client.topics


def test_multi_subscribe_run():
    new_mc = mqtt_client.Mqtt_Client("LWT_test")
    sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslcontext.load_cert_chain(
        certfile=conf.get("certfile", ""),
        keyfile=conf.get("keyfile"),
        password=conf.get("password"),
    )
    new_mc.configure(
        conf.get("mqtt_server"), conf.get("mqtt_port"), sslcontext=sslcontext
    )
    subscription_counter = 0

    def __cb_on_subscribe(client, userdata, mid, granted_qos):
        nonlocal subscription_counter
        subscription_counter += 1

    new_mc.on_subscribe = __cb_on_subscribe
    new_mc.run("Notifier/A", "Notifier/B", "Notifier/C")
    time.sleep(1)
    assert subscription_counter == 3


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


def test_lwt(get_mqtt_client: mqtt_client.Mqtt_Client):
    """Creating two connections. One to monitor Last Will from the other.
    "LWT_test" is the additional created connection, that gets created and
    reports online and offline to "code/status/connection"


    Args:
        get_mqtt_client (mqtt_client.Mqtt_Client): monitoring mqtt client
    """
    lwt = "code/status/connection"
    get_mqtt_client.subscribe(lwt)
    response = b""

    def __cb_on_message(mqttc, obj, msg):
        nonlocal response
        response = msg.payload

    get_mqtt_client.on_message = __cb_on_message
    new_mc = mqtt_client.Mqtt_Client("LWT_test")
    sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslcontext.load_cert_chain(
        certfile=conf.get("certfile", ""),
        keyfile=conf.get("keyfile"),
        password=conf.get("password"),
    )
    new_mc.configure(
        conf.get("mqtt_server"), conf.get("mqtt_port"), sslcontext=sslcontext
    )
    new_mc.will_set(lwt, payload="Offline", retain=False)
    new_mc.will_send_online = True
    new_mc.run()
    print("Wait for connection ", end="")
    while not new_mc.connected:
        print(".", end="")
        time.sleep(1)
    print(" connected.")
    time.sleep(1)
    assert response.decode() == "Online"
    response = b""
    print("Wait for connection STOP")
    new_mc._sock_close()
    new_mc.loop_stop()
    while not response.decode() == "Offline":
        print(".", end="")
        time.sleep(1)
    print(" STOPPED")

    time.sleep(1)
    assert get_mqtt_client.connected is True
    assert response.decode() == "Offline"
