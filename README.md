# mqtt_tree / mqtt_client

## mqtt_client
Wrapepr around paho/mqtt_client to easier handle certifacte based authentication and connection to mqtt via a python queue.
I use this wrapper in serveral internal projects to simplify the handling. 

## mqtt_tree 
As I didn't found a light wight way to keep an overview of all topic published from various devices I wrote a small python UI.

## change log
2021=01-31 BREAKING Change: moved files to create a python package; Version 0.1.1
2019-03-11 config via config.py
2019-02-28 ssl client certificate support
2019-02-15 initial version


## Installation
pip install git+https://github.com/poggenpower/mqtt_tree

## Setup
copy config.py.example to config.py
and change for your needs.

## Run
`python mqtt_tree.py` should do the job.

### How it looks like
![mqtt_tree](https://user-images.githubusercontent.com/6035034/53057173-831a3f00-34ae-11e9-8a76-a66edc996c21.png)

nothing fancy, just an overview.

### How it works

It subscribes '#', means any topic and keep listening for changes and new topics, while in parallel feeding to received topics in the treeview of an very basic TKinter Application.
It doesn't "forget" any Topics while running, which makes it useful to monitor, whats there only temporary.

Feedback, Issues, Suggestions, Improvements, Forks all welcome. Use the Issue tracker here to get in contact.

## Todo / Know Issues
* allow ssl without client certificate
* grey out non retaining topics after a while. 

##### Hidden Features ;-)

If the window is closed, it writes the actual tree content to stdout. Not sure if it is useful for someone.
