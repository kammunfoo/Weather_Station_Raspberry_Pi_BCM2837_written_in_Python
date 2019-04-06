#!/usr/bin/python3

"""
Assignment #9 - publish pubnub
UCSC IoT 30402
Gil Garcia
"""
import time
import datetime
import sys
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
dt=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

#setup
pubconf = PNConfiguration()
pubconf.subscribe_key='sub-c-53844344-2163-11e8-be22-c2fd0b475b93'
pubconf.publish_key='pub-c-3a8a789c-c79c-4b57-9eb8-c1de665ec9f6'
pubnub = PubNub(pubconf)

#assign a channel
channel = 'Weather_Station'

#callback section
def publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        # Message successfully published to specified channel.
        print("Message Sent")
    else:
        # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
        print("Error Sending!")

#assign some data
#data = ['35.6,29.95']
data1 = 'Hello, How are you?' + ' ' + dt
#data2 = '\n'

# now send something!!!
#pubnub.publish().channel(channel).message(data).async(publish_callback)
pubnub.publish().channel(channel).message(data1).async(publish_callback)
#pubnub.publish().channel(channel).message(data2).async(publish_callback)

