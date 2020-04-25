#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
"""
Python lambda functions should use this for logging configuration.
The intent is to centralize and capture data as JSON.
"""

# Get existing log handlers and remove them (start fresh)
logger = logging.getLogger()
for ch in logger.handlers:
    logger.removeHandler(ch)

# Create a channel for the logger
ch = logging.StreamHandler()

# Define a logging format to use (JSON)
formatter = logging.Formatter(
    (
        '{"unix_time":%(created)s, "time":"%(asctime)s", "module":"%(name)s",'
        ' "line_no":%(lineno)s, "level":"%(levelname)s", "msg":"%(message)s"},'
    )
)

# Set the handler's log format
ch.setFormatter(formatter)

# Set the log_level and connect the handler to the channel
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

# Define log_levels for modules where appropriate
logging.getLogger('__name__').addHandler(logging.NullHandler())
logging.getLogger('__main__').setLevel(logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.WARN)
