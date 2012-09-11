#!/usr/bin/python
# -*- coding: utf-8 -*-

from logbook import NestedSetup, NullHandler, FileHandler, MailHandler


class LogbookConfig(object):

    def __init__(self, name, debug = False):
        self.debug_enabled = debug
        path_tmpl = 'log/{name}_{level}.log'
        mail_tmpl = '{name}_error@localhost'
        self.debug = path_tmpl.format(name = name, level = 'debug')
        self.info = path_tmpl.format(name = name, level = 'info')
        self.warn = path_tmpl.format(name = name, level = 'warn')
        self.err = path_tmpl.format(name = name, level = 'err')
        self.crit = path_tmpl.format(name = name, level = 'crit')
        self.from_mail = mail_tmpl.format(name = name)
        self.to_mails = ['me@localhost']
        self.smtp_server = 'localhost'

    def setup(self):
        # a nested handler setup can be used to configure more complex setups
        setup = [
            # make sure we never bubble up to the stderr handler
            # if we run out of setup handling
            NullHandler(),
            # then write messages that are at least info to to a logfile
            FileHandler(self.info, level='INFO', encoding='utf-8'),
            # then write messages that are at least warnings to to a logfile
            FileHandler(self.warn, level='WARNING', encoding='utf-8'),
            # then write messages that are at least errors to to a logfile
            FileHandler(self.err, level='ERROR', encoding='utf-8'),
            # then write messages that are at least critical errors to to a logfile
            FileHandler(self.crit, level='CRITICAL', encoding='utf-8'),
            # errors should then be delivered by mail and also be kept
            # in the application log, so we let them bubble up.
            #MailHandler(self.from_mail, self.to_mails, level='ERROR',
            #    bubble=True, server_addr=(self.smtp_server, 25))
        ]
        if self.debug_enabled:
            setup.insert(1, FileHandler(self.debug, level='DEBUG', encoding='utf-8'))
        return NestedSetup(setup)
