#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import argparse
import time

parser = argparse.ArgumentParser(description='Configure a logging publisher.')

parser.add_argument("-H", "--hostname", default='localhost', type=str, help='Set the hostname of the server.')
parser.add_argument("-p", "--port", default=6379, type=int, help='Set the server port.')
parser.add_argument("-c", "--channel",type=str, help='Channel to publish into.')

args = parser.parse_args()

r = redis.StrictRedis(host=args.hostname, port=args.port, db=0)

for i in range(0,21):
    if i%2 == 0 :
        r.publish(args.channel + '.INFO', 'test' + str(i))
    elif i%3 == 0 :
        r.publish(args.channel + '.WARNING', 'test' + str(i))
    elif i%5 == 0:
        r.publish(args.channel + '.ERROR', 'test' + str(i))
    elif i%7 == 0:
        r.publish(args.channel + '.CRITICAL', 'test' + str(i))
    else:
        r.publish(args.channel + '.DEBUG', 'test' + str(i))


    time.sleep(1)
