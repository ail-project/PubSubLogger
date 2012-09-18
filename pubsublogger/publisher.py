#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:mod:`publisher` -- Publish logging messages on a redis channel

To use this module, you have to define at least a channel name.

.. note::
    The channel name should represent the area of the program you want
    to log. It can be whatever you want.


"""

import redis

from pubsublogger.exceptions import InvalidErrorLevel, NoChannelError

hostname = 'localhost'
port = 6379
channel = None
redis_instance = None

__error_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


def __connect():
    """
    Connect to a redis instance.
    """
    global redis_instance
    redis_instance = redis.StrictRedis(host=hostname, port=port)


def log(level, message):
    """
    Publish `message` with the `level` the redis `channel`.

    :param level: the level of the message
    :param message: the message you want to log
    """
    if redis_instance is None:
        __connect()

    if level not in __error_levels:
        raise InvalidErrorLevel('You have used an invalid error level. \
                Please choose in: ' + ', '.join(__error_levels))
    if channel is None:
        raise NoChannelError('Please set a channel.')
    c = '{channel}.{level}'.format(channel=channel, level=level)
    redis_instance.publish(c, message)


def debug(message):
    """
    Publush a DEBUG `message`
    """
    log('DEBUG', message)


def info(message):
    """
    Publush an INFO `message`
    """
    log('INFO', message)


def warning(message):
    """
    Publush a WARNING `message`
    """
    log('WARNING', message)


def error(message):
    """
    Publush an ERROR `message`
    """
    log('ERROR', message)


def critical(message):
    """
    Publush a CRITICAL `message`
    """
    log('CRITICAL', message)


