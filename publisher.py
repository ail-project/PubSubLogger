#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis

hostname = 'localhost'
port = 6379
channel = None
redis_instance = None

def connect():
    global hostname
    global port
    global redis_instance
    redis_instance = redis.StrictRedis(host=hostname, port=port)

def log(level, message):
    global channel
    if redis_instance is not None and channel is not None:
        c = '{channel}.{level}'.format(channel = channel, level = level)
        redis_instance.publish(c, message)

def debug(message):
    log('DEBUG', message)

def info(message):
    log('INFO', message)

def warning(message):
    log('WARNING', message)

def error(message):
    log('ERROR', message)

def critical(message):
    log('CRITICAL', message)



if __name__ == '__main__':
    import argparse
    import time

    parser = argparse.ArgumentParser(description='Configure a logging publisher.')

    parser.add_argument("-H", "--hostname", default='localhost', type=str, help='Set the hostname of the server.')
    parser.add_argument("-p", "--port", default=6379, type=int, help='Set the server port.')
    parser.add_argument("-c", "--channel",type=str, required=True, help='Channel to publish into.')

    args = parser.parse_args()

    channel = args.channel
    hostname = args.hostname
    port = args.port

    connect()
    for i in range(0,21):
        if i%2 == 0 :
            info('test' + str(i))
        elif i%3 == 0 :
            warning('test' + str(i))
        elif i%5 == 0:
            error('test' + str(i))
        elif i%7 == 0:
            critical('test' + str(i))
        else:
            debug('test' + str(i))
        time.sleep(1)
