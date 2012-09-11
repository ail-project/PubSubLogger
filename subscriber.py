#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal
import sys
import time
import redis
from logbook import Logger
import ConfigParser

import logbook_config

redis_host = 'localhost'
redis_port = 6379
pubsub = None
channel = None

def signal_handler(signal, frame):
    global pubsub
    global channel
    if pubsub is not None:
        pubsub.punsubscribe(channel)
        print "Subscriber closed."
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def mail_setup(path):
    config = ConfigParser.RawConfigParser()
    config.readfp(path)
    logbook_config.dest_mails = config.get('mail', 'dest_mail').split(',')
    logbook_config.smtp_server = config.get('mail', 'smtp_server')
    logbook_config.smtp_port = config.get('mail', 'smtp_port')
    logbook_config.src_server = config.get('mail', 'src_server')

def run(log_name, path, debug = False, mail = None):
    global pubsub
    global channel
    channel = log_name
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    pubsub = r.pubsub()
    pubsub.psubscribe(channel + '.*')

    logger = Logger(channel)
    if mail is not None:
        mail_setup(mail)
    with logbook_config.setup(channel, path, debug):
        for msg in pubsub.listen():
            if msg['type'] == 'pmessage':
                level = msg['channel'].split('.')[1]
                message = msg['data']
                logger.log(level, message)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Configure a logging subscriber.')

    parser.add_argument("-H", "--hostname", default='localhost',
            type=str, help='Set the hostname of the server.')
    parser.add_argument("-p", "--port", default=6379,
            type=int, help='Set the server port.')
    parser.add_argument("-c", "--channel",
            type=str, required=True, help='Channel to subscribe to.')
    parser.add_argument("-l", "--log_path",
            required=True, help='Path where the logs will be written')
    parser.add_argument("-d", "--debug", action="store_true",
            help='Also log debug messages.')
    parser.add_argument("-m", "--mail", type=file, default=None,
            help='Path to the config file used to send errors by email.')

    args = parser.parse_args()

    redis_host = args.hostname
    redis_port = args.port
    run(args.channel, args.log_path, args.debug, args.mail)

