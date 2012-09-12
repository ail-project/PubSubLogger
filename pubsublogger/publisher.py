#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis

hostname = 'localhost'
port = 6379
channel = None
redis_instance = None

def connect():
    global redis_instance
    redis_instance = redis.StrictRedis(host=hostname, port=port)

def log(level, message):
    if redis_instance is not None and channel is not None:
        c = '{channel}.{level}'.format(channel = channel, level = level)
        redis_instance.publish(c, message)
    else:
        raise Exception('Not connected to redis and/or no channel set')

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
