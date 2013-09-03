#!/usr/bin/env python
# encoding: utf-8

# position.py
# 
# Created by Maan Bsat on 2013-09-02.
# Copyright (c) 2013 Maan Bsat. All rights reserved.


from untws.instrument import create_instrument

class Position(object):
    """Represents a single position"""
    
    def __init__(self, connection, account_name, instrument, quantity, price,
        average_cost, market_value, realized_pnl, unrealized_pnl):
        self._connection = connection
        self._account_name = account_name
        self._instrument = create_instrument(connection, instrument)
        self._quantity = quantity
        self._price = price
        self._average_cost = average_cost
        self._market_value = market_value
        self._realized_pnl = realized_pnl
        self._unrealized_pnl = unrealized_pnl
    
    def __repr__(self):
        return "<Position(%s, %s, %f)>" % \
            (self.account_name, self.instrument.ticker, self.quantity)
    
    @property
    def connection(self):
        """Returns the connection object"""
        return self._connection
    
    @property
    def account_name(self):
        """The account name for this position"""
        return self._account_name

    @property
    def instrument(self):
        """The instrument object"""
        return self._instrument

    @property
    def quantity(self):
        """The position quantity"""
        return self._quantity

    @property
    def price(self):
        """The current price"""
        return self._price

    @property
    def average_cost(self):
        """The average cose"""
        return self._average_cost

    @property
    def market_value(self):
        """The market value"""
        return self._market_value

    @property
    def realized_pnl(self):
        """The realized P&L"""
        return self._realized_pnl

    @property
    def unrealized_pnl(self):
        """The unrealized P&L"""
        return self._unrealized_pnl
