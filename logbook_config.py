#!/usr/bin/python
# -*- coding: utf-8 -*-

from logbook import NestedSetup, NullHandler, FileHandler, MailHandler
import os

dest_mails = []
smtp_server = None
smtp_port = 0
src_server = None

def setup(name, path = 'log', enable_debug = False):
    path_tmpl = os.path.join(path, '{name}_{level}.log')
    info = path_tmpl.format(name = name, level = 'info')
    warn = path_tmpl.format(name = name, level = 'warn')
    err = path_tmpl.format(name = name, level = 'err')
    crit = path_tmpl.format(name = name, level = 'crit')
    # a nested handler setup can be used to configure more complex setups
    setup = [
        # make sure we never bubble up to the stderr handler
        # if we run out of setup handling
        NullHandler(),
        # then write messages that are at least info to to a logfile
        FileHandler(info, level='INFO', encoding='utf-8'),
        # then write messages that are at least warnings to to a logfile
        FileHandler(warn, level='WARNING', encoding='utf-8'),
        # then write messages that are at least errors to to a logfile
        FileHandler(err, level='ERROR', encoding='utf-8'),
        # then write messages that are at least critical errors to to a logfile
        FileHandler(crit, level='CRITICAL', encoding='utf-8'),
    ]
    if enable_debug:
        debug = path_tmpl.format(name = name, level = 'debug')
        setup.insert(1, FileHandler(debug, level='DEBUG', encoding='utf-8'))
    if src_server is not None and smtp_server is not None \
            and smtp_port != 0 and len(dest_mails) != 0:
        mail_tmpl = '{name}_error@{src}'
        from_mail = mail_tmpl.format(name = name, src = src_server)
        print from_mail
        # errors should then be delivered by mail and also be kept
        # in the application log, so we let them bubble up.
        setup.append(MailHandler(from_mail, dest_mails, level='ERROR',
            bubble=True, server_addr=(smtp_server, smtp_port)))

    return NestedSetup(setup)
