#!/usr/bin/env python
# encoding: utf-8

# market_data.py
# 
# Created by Maan Bsat on 2013-09-03.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

class MarketDataQuote(object):
    """Represents a market data quote"""
    
    def __init__(self, instrument, data_points):
        self._instrument = instrument
        self._data_points = data_points
    
    @property
    def instrument(self):
        """The instrument object"""
        return self._instrument
    
    @property
    def available_fields(self):
        """
        Returns a list of the available quote fields
        (e.g. 'bid', 'ask', etc.)
        """
        return self._data_points.keys()
    
    def __getattr__(self, field):
        return self.get(field)
    
    def get(self, field):
        if field not in self._data_points:
             raise AttributeError(
                 'Quote does not contain element "%s"' % field
             )
        return self._data_points[field]
