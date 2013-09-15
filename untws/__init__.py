#!/usr/bin/env python
# encoding: utf-8

# __init__.py
# 
# Created by Maan Bsat on 2013-09-02.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

"""
"Pythonic" access to Interactive Brokers TWS (uses IbPy)
"""

import os
from untws.connection import IBConnection

__all__ = ['ib_connect']

def ib_connect(hostname=None, port=None):
    """
    Returns a connection object to IB TWS.
    
    If *hostname* is *None*, it will first look for the *IB_HOSTNAME*
    environment variable, else it will default to *localhost*.
    If *port* is *None*, it will first look for the *IB_PORT*
    environment variable, else it will default to *7496*.
    """
    if hostname is None:
        if 'IB_HOSTNAME' in os.environ:
            hostname = os.environ['IB_HOSTNAME']
        else:
            hostname = 'localhost'
    if port is None:
        if 'IB_PORT' in os.environ:
            port = os.environ['IB_PORT']
        else:
            port = 7496
    return IBConnection(
        hostname=hostname,
        port=port
    )
