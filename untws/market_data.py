#!/usr/bin/env python
# encoding: utf-8

# market_data.py
# 
# Created by Maan Bsat on 2013-09-03.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

__all__ = [
    'MarketDataQuoteBase', 'MarketDataQuoteInstrument', 'OptionDataQuote'
]

class MarketDataQuoteBase(object):
    """Represents a market data quote"""
    
    def __init__(self, data_points):
        self._data_points = data_points
    
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

class MarketDataQuoteInstrument(MarketDataQuoteBase):
    def __init__(self, instrument, data_points):
        super(MarketDataQuoteInstrument, self).__init__(self, data_points)
        self._instrument = instrument

    @property
    def instrument(self):
        """The instrument object"""
        return self._instrument

class OptionDataQuote(MarketDataQuoteBase):
    def __init__(self, data_points):
        super(OptionDataQuote, self).__init__(self, data_points)

    @property
    def mid(self):
        if 'mid' in self.available_fields:
            return self.get('mid')
        if not (
            'bid' in self.available_fields and 
            'ask' in self.available_fields
        ):
            raise Exception(
                "Mid is only available if both Bid and Ask are available"
            )
        # construct the mid point
        mid = {}
        for f in self.bid.available_fields:
            if f in self.ask.available_fields:
                mid[f] = (self.bid.get(f) + self.ask.get(f)) / 2
        self._data_points['mid'] = MarketDataQuoteBase(mid)
        return self.get('mid')