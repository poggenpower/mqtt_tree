# mqtt_tree

As I didn't found a light wight way to keep an overview of all topic published from various devices I wrote a small python UI.

## Installation
* install the paho-mqtt module e.g. via pip:
  * `pip install paho-mqtt`
* copy all files from this repo e.g. via git
  * `git clone ....`

## Setup
as this is in a really early stage setup is a little bit rough.
Change the line `self.connect("haus.wupp", 1883, 60)` in file `mqtt_client.py` to your needs. For option check the paho documentation.

## Run
`python mqtt_tree.py` should do the job.

### How it looks like
...
