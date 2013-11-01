#!/usr/bin/env python
# encoding: utf-8

# historical_data.py
# 
# Created by Maan Bsat on 2013-11-01.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

from datetime import date, datetime

__all__ = [
    'HistoricalDataPoint'
]

def parse_date(s):
    if len(s) == 8:
        return date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    else:
        (dt, tm) = [x for x in s.split(' ') if len(x) > 0]
        return datetime(
            int(dt[0:4]),
            int(dt[4:6]),
            int(dt[6:8]),
            int(tm[0:2]),
            int(tm[3:5]),
            int(tm[6:8])
        )

class HistoricalDataPoint(object):
    """Represents a market data quote"""
    
    def __init__(self, msg):
        self._date = parse_date(msg.date)
        self._open = msg.open
        self._high = msg.high
        self._low = msg.low
        self._close = msg.close
        self._volume = msg.volume
        self._count = msg.count
        self._WAP = msg.WAP
        self._has_gaps = msg.hasGaps
    
    @property
    def date(self):
        return self._date
        
    @property
    def open(self):
        return self._open

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low

    @property
    def close(self):
        return self._close
        
    @property
    def volume(self):
        return self._volume
        
    @property
    def count(self):
        return self._count

    @property
    def WAP(self):
        return self._WAP

    @property
    def has_gaps(self):
        return self._has_gaps
