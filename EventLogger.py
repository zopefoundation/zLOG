##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""
A logging module which handles event messages.

This uses Vinay Sajip's PEP 282 logging module.
"""

__version__='$Revision$'[11:-2]

import os, sys, time
import logging
from BaseLogger import BaseLogger
from LogHandlers import FileHandler, NullHandler, SysLogHandler
from logging import StreamHandler, Formatter

class EventLogger(BaseLogger):

    # Get our logger object:
    logger = logging.getLogger('event')
    # Add a null handler to prevent warnings about loggers with no handlers:
    logger.addHandler(NullHandler())

    def log(self, subsystem, severity, summary, detail, error):

        level = (zlog_to_pep282_severity_cache_get(severity) or
                 zlog_to_pep282_severity(severity))

        # Try an early exit if the logger is disabled for this level.
        # (XXX This inlines logger.isEnabledFor(level).)
        if (self.logger.manager.disable >= level or
            level < self.logger.getEffectiveLevel()):
            return

        msg = "%s %s %s" % (
            severity_string_cache_get(severity) or severity_string(severity),
            subsystem,
            summary)

        if detail:
            msg = "%s\n%s" % (msg, detail)

        self.logger.log(level, msg, exc_info=(error is not None))

event_logger = EventLogger()

log_write = event_logger.log

def severity_string(severity, mapping={
    -300: 'TRACE',
    -200: 'DEBUG',
    -100: 'BLATHER',
       0: 'INFO',
     100: 'PROBLEM',
     200: 'ERROR',
     300: 'PANIC',
    }):
    """Convert a severity code to a string."""
    s = mapping.get(int(severity), '')
    return "%s(%s)" % (s, severity)

severity_string_cache = {}
for _sev in range(-300, 301, 100):
    severity_string_cache[_sev] = severity_string(_sev)
severity_string_cache_get = severity_string_cache.get

def zlog_to_pep282_severity(zlog_severity):
    """
    We map zLOG severities to PEP282 severities here.
    This is how they are mapped:

    zLOG severity                      PEP282 severity
    -------------                      ---------------
    PANIC (300)                        critical (50)
    ERROR (200), PROBLEM (100)         error (40)
    INFO (0)                           warn (30)
    BLATHER (-100)                     info (20)
    DEBUG (-200), TRACE (-300)         debug (10)
    """
    sev = zlog_severity
    if sev >= 300:
        return logging.CRITICAL
    if sev >= 100:
        return logging.ERROR
    if sev >= 0:
        return logging.WARN
    if sev >= -100:
        return logging.INFO
    else:
        return logging.DEBUG

zlog_to_pep282_severity_cache = {}
for _sev in range(-300, 301, 100):
    zlog_to_pep282_severity_cache[_sev] = zlog_to_pep282_severity(_sev)
zlog_to_pep282_severity_cache_get = zlog_to_pep282_severity_cache.get

def log_time():
    """Return a simple time string without spaces suitable for logging."""
    return ("%4.4d-%2.2d-%2.2dT%2.2d:%2.2d:%2.2d"
            % time.localtime()[:6])

def get_env_severity_info():
    # EVENT_LOG_SEVERITY is the preferred envvar, but we accept
    # STUPID_LOG_SEVERITY also
    eget = os.environ.get
    severity = eget('EVENT_LOG_SEVERITY') or eget('STUPID_LOG_SEVERITY')
    if severity:
        severity = int(severity)
    else:
        severity = 0 # INFO
    return severity

def get_env_syslog_info():
    eget = os.environ.get
    addr = None
    port = None
    path = eget('ZSYSLOG')
    facility = eget('ZSYSLOG_FACILITY', 'user')
    server = eget('ZSYSLOG_SERVER')
    if server:
        addr, port = server.split(':')
        port = int(port)
    if addr:
        return (facility, (addr, port))
    else:
        return (facility, path)

def get_env_file_info():
    eget = os.environ.get
    # EVENT_LOG_FILE is the preferred envvar, but we accept
    # STUPID_LOG_FILE also
    path = eget('EVENT_LOG_FILE')
    if path is None:
        path = eget('STUPID_LOG_FILE')
    if path is None:
        dest = None
    else:
        dest = path
    return dest

formatters = {
    'file':    Formatter(fmt='------\n%(asctime)s %(message)s',
                         datefmt='%Y-%m-%dT%H:%M:%S'),
    'syslog':  Formatter(fmt='%(message)s'),
    }

def initialize_from_environment():
    """ Reinitialize the event logger from the environment """
    # clear the current handlers from the event logger
    event_logger.logger.handlers = []

    handlers = []

    # set up syslog handler if necessary
    facility, syslogdest = get_env_syslog_info()
    if syslogdest:
        handler = SysLogHandler(syslogdest, facility)
        handler.setFormatter(formatters['syslog'])
        handlers.append(handler)

    # set up file handler if necessary
    filedest = get_env_file_info()
    if filedest:
        handler = FileHandler(filedest)
        handler.setFormatter(formatters['file'])
        handlers.append(handler)
    elif filedest == '':
        # if dest is an empty string, log to standard error
        handler = StreamHandler()
        handler.setFormatter(formatters['file'])
        handlers.append(handler)
    else:
        # log to nowhere, but install a 'null' handler in order to
        # prevent error messages from emanating due to a missing handler
        handlers.append(NullHandler())

    severity = get_env_severity_info()
    severity = zlog_to_pep282_severity(severity)
    event_logger.logger.setLevel(severity)

    for handler in handlers:
        event_logger.logger.addHandler(handler)