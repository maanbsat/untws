#!/usr/bin/env python
# encoding: utf-8
"""
instrument.py

Created by Maan Bsat on 2013-09-02.
Copyright (c) 2013 Maan Bsat. All rights reserved.
"""

from datetime import datetime, date

__all__ = ['create_instrument', 'Instrument', 'Stock', 'StockOption']

def create_instrument(connection, instrument):
    if instrument.m_secType == 'STK':
        return Stock(connection, instrument)
    elif instrument.m_secType == 'OPT':
        return StockOption(connection, instrument)
    else:
        raise Exception("Do not know how to handle instrument of type %s: %s" % (i.m_secType, i.m_localSymbol))

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
        return self._connection
    
    @property
    def ticker(self):
        return self._ticker
    
    @property
    def conid(self):
        return self._conid

    @property
    def currency(self):
        return self._currency

    @property
    def exchange(self):
        return self._exchange
    
    def __repr__(self):
        return "<%s(%s)>" % (str(type(self)), self.ticker)
        
class Stock(Instrument):
    def __init__(self, connection, instrument):
        super(Stock, self).__init__(connection, instrument)

class StockOption(Instrument):
    def __init__(self, connection, instrument):
        super(StockOption, self).__init__(connection, instrument)
        self._underlying = instrument.m_symbol
        self._contract_size = instrument.m_multiplier
        self._option_type = 'call' if instrument.m_right == 'C' else 'put'
        self._strike_price = instrument.m_strike
        self._expiration_date = datetime.strptime(instrument.m_expiry, '%Y%m%d').date()
    
    @property
    def underlying(self):
        return self._underlying
        
    @property
    def contract_size(self):
        return self._contract_size

    @property
    def option_type(self):
        return self._option_type
        
    @property
    def strike_price(self):
        return self._strike_price
        
    @property
    def expiration_date(self):
        return self._expiration_date
