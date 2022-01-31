import mqtt_client
import time
import tk_tree
import threading
import ssl
import sys
import logging
logger = logging.getLogger(__name__)

from config import conf


class mqtt_path_element():
    TYPE_BRANCH = 1
    TYPE_LEAF = 2

    def __init__(self, name, tree_id=None, ptype=0):
        self.children = dict()
        self.nane = 'unknown'
        self.name = name
        self.tree_id = tree_id
        self.type = ptype

    def set_type(self, ptype):
        self.type = ptype

    def set_payload(self, qos, payload):
        self.qos = qos
        self.payload = payload

    def add_child(self, child):
        # print("I am {} My Childs are: {}"
        #       .format(self.name, ", ".join(map(str, self.get_children()))))
        self.children[child.name] = child

    def get_children(self):
        return self.children.values()

    def get_child(self, name):
        return self.children[name]

    def is_child(self, name):
        return name in self.children

    def __str__(self):
        return self.name


def read_mqtt_q(q, mqtt_root, app):
    while True:
        print("read_mqtt_q: wainting for new message")
        msg = q.get()
        if isinstance(msg, bool):
            break
        # print("woring on topic: {}".format(msg.topic))
        mqtt_path = msg.topic
        mqtt_path_split = mqtt_path.split('/')
        i = 0
        parent = mqtt_root
        for element in mqtt_path_split:
            i += 1
            if not parent.is_child(element):
                if parent.name == 'root':
                    id = app.tree_insert("", "end", None, text=element)
                else:
                    if i >= len(mqtt_path_split):
                        id = app.tree_insert(
                            parent.tree_id,
                            "end", None,
                            text=element,
                            values=(msg.qos, msg.retain, msg.payload)
                        )
                    else:
                        id = app.tree_insert(parent.tree_id, "end", None, text=element)
                child = mqtt_path_element(element, tree_id=id)
                parent.add_child(child)
            else:
                child = parent.get_child(element)
                # Update child, if a TYPE_LEAF
                if i >= len(mqtt_path_split):
                    app.item_update(child.tree_id, (msg.qos, msg.retain, msg.payload))
                # print("My Parent is {} and has this childs: {}"
                #       .format(parent.name, ", ".join(map(str,parent.get_children()))))
            parent = child


def print_topics(root, level):
    for child in root.get_children():
        print('  ' * level + child.name)
        print_topics(child, level + 1)


handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(handlers=[handler, ], level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger()

sslcontext = None
if conf.get('ssl'):
    sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslcontext.load_cert_chain(
        certfile=conf.get('certfile'),
        keyfile=conf.get('keyfile'),
        password=conf.get('password'),
    )
# (password=XXX) givs pw for keyfiles. Key can be in the CA file, but first.

mc = mqtt_client.Mqtt_Client("mqtt_tree")
mc.configure(conf.get('mqtt_server'), conf.get('mqtt_port'), sslcontext=sslcontext)
q = mc.get_queue()
mc.run('#')

app = tk_tree.TK_Tree()

print("Queuesize: {}".format(q.qsize()))
mqtt_root = mqtt_path_element('root')
print('Root Element created')
# read_mqtt_q(q, mqtt_root, app)
receive_thread = threading.Thread(target=read_mqtt_q, args=(q, mqtt_root, app))
print('Starting MQTT event processing in the background')
receive_thread.start()

app.run()

mc.loop_stop()
q.put(False)  # Stop Threat
print_topics(mqtt_root, 1)

print('########################################################################')
