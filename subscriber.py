#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import argparse
import time

from logbook_config import LogbookConfig
from logbook import Logger

parser = argparse.ArgumentParser(description='Configure a logging subscriber.')

parser.add_argument("-H", "--hostname", default='localhost', type=str, help='Set the hostname of the server.')
parser.add_argument("-p", "--port", default=6379, type=int, help='Set the server port.')
parser.add_argument("-c", "--channel", type=str, help='Channel to subscribe to.')
parser.add_argument("-d", "--debug", action="store_true", help='Also log debug messages.')

args = parser.parse_args()

r = redis.StrictRedis(host=args.hostname, port=args.port, db=0)
pubsub = r.pubsub()
pubsub.psubscribe(args.channel + '.*')

log_config = LogbookConfig(args.channel, args.debug)

while 1:
    logger = Logger(args.channel)
    with log_config.setup():
        for msg in pubsub.listen():
            if msg['type'] == 'pmessage':
                level = msg['channel'].split('.')[1]
                message = msg['data']
                logger.log(level, message)
        time.sleep(10)
