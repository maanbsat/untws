#!/usr/bin/env python
# encoding: utf-8

# instrument.py
# 
# Created by Maan Bsat on 2013-09-02.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

from datetime import datetime, date

__all__ = ['create_instrument', 'Instrument', 'Stock', 'StockOption']

def create_instrument(connection, instrument):
    if instrument.m_secType == 'STK':
        return Stock(connection, instrument)
    elif instrument.m_secType == 'OPT':
        return StockOption(connection, instrument)
    else:
        raise Exception(
            "Do not know how to handle instrument of type %s: %s" % \
            (instrument.m_secType, instrument.m_localSymbol)
        )

class Instrument(object):
    """Represents an (abstract) instrument"""
    
    def __init__(self, connection, instrument):
        self._connection = connection
        self._ticker = instrument.m_localSymbol
        self._conid = instrument.m_conId
        self._currency = instrument.m_currency
        self._exchange = instrument.m_primaryExch
    
    @property
    def connection(self):
        """Returns the connection object"""
        return self._connection
    
    @property
    def ticker(self):
        """The instrument ticker"""
        return self._ticker
    
    @property
    def conid(self):
        """The IB contract id for this instrument (the 'conid')"""
        return self._conid

    @property
    def currency(self):
        """The instrument's currency"""
        return self._currency

    @property
    def exchange(self):
        """The instrument's primary exchange"""
        return self._exchange
    
    def __repr__(self):
        return "<%s(%s)>" % (str(type(self)), self.ticker)
        
class Stock(Instrument):
    """Represents a stock (IB sectype: STK)"""
    
    def __init__(self, connection, instrument):
        super(Stock, self).__init__(connection, instrument)

class StockOption(Instrument):
    """Represents a stock option (IB sectype: OPT)"""
    
    def __init__(self, connection, instrument):
        super(StockOption, self).__init__(connection, instrument)
        self._underlying = instrument.m_symbol
        self._contract_size = instrument.m_multiplier
        self._option_type = 'call' if instrument.m_right == 'C' else 'put'
        self._strike_price = instrument.m_strike
        self._expiration_date = datetime.strptime(
            instrument.m_expiry,
            '%Y%m%d'
        ).date()
    
    @property
    def underlying(self):
        """The underlying equity ticker"""
        return self._underlying
        
    @property
    def contract_size(self):
        """The contract size (i.e. multiplier)"""
        return self._contract_size

    @property
    def option_type(self):
        """The option type ('call' or 'put')"""
        return self._option_type
        
    @property
    def strike_price(self):
        """The option's strike price"""
        return self._strike_price
        
    @property
    def expiration_date(self):
        """The option's expiration date"""
        return self._expiration_date
