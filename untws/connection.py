#!/usr/bin/env python
# encoding: utf-8

# connection.py
# 
# Created by Maan Bsat on 2013-09-02.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

from Queue import Queue
from random import randint
from datetime import datetime
import ib.opt
from ib.opt import message
from ib.ext.Contract import Contract
from untws.position import Position
from untws.market_data import *

MKT_DATA_FIELDS = {
    1: 'bid',
    2: 'ask',
    4: 'last',
    6: 'high',
    7: 'low',
    9: 'close'
}

OPT_DATA_FIELDS = {
    10: 'bid',
    11: 'ask',
    12: 'last',
    13: 'model'
}

class IBConnection(object):
    """This is the core object which represents a connection to IB."""

    def __init__(self, host, port):
        self.connection = ib.opt.ibConnection(
            host=host,
            port=port,
            clientId=randint(1000, 99999)
        )
        self.connection.connect()
        
        self._messages = Queue()
    
    def _process_message(self, msg):
        """Callback for ibpy"""
        self._messages.put(msg)

    def get_current_time(self):
        """
        Returns the current TWS server time, as a *datetime.date* object.
        """
        self.connection.register(self._process_message, message.currentTime)
        self.connection.reqCurrentTime()
        msg = self._messages.get()
        assert isinstance(msg, message.currentTime)
        self.connection.unregister(self._process_message, message.currentTime)
        return datetime.fromtimestamp(msg.time)
        
    def get_positions(self):
        """
        Returns a list of positions.
        """
        self.connection.register(
            self._process_message,
            'UpdatePortfolio',
            'AccountDownloadEnd'
        )
        self.connection.reqAccountUpdates(1, '')
        out = []
        while True:
            msg = self._messages.get()
            if msg.typeName == 'accountDownloadEnd':
                break
            assert msg.typeName == 'updatePortfolio'
            out.append(Position(
                self,
                msg.accountName,
                msg.contract,
                msg.position,
                msg.marketPrice,
                msg.averageCost,
                msg.marketValue,
                msg.realizedPNL,
                msg.unrealizedPNL
            ))
        self.connection.reqAccountUpdates(0, '')
        self.connection.unregister(
            self._process_message,
            'UpdatePortfolio',
            'AccountDownloadEnd'
        )
        return out
    
    def get_market_data(self, instrument):
        """
        Request the current market data for an instrument (contract). Instrument
        can be obtained by *create_stock* and *create_option_ticker*.
        """
        self.connection.register(
            self._process_message,
            message.tickPrice,
            message.tickSnapshotEnd,
            message.tickOptionComputation
        )
        # request a "non-subscription" market data quote
        self.connection.reqMktData(1, instrument, '', True)
        data = {}
        opts = {}
        while True:
            msg = self._messages.get()
            if isinstance(msg, message.tickSnapshotEnd):
                break
            elif isinstance(msg, message.tickPrice):
                if msg.field not in MKT_DATA_FIELDS:
                    # we ignore fields that we don't know of
                    continue
                data[MKT_DATA_FIELDS[msg.field]] = msg.price
            elif isinstance(msg, message.tickOptionComputation):
                if msg.field not in OPT_DATA_FIELDS:
                    # we ignore fields that we don't know of
                    continue
                opts[OPT_DATA_FIELDS[msg.field]] = MarketDataQuoteBase({
                    'price': msg.optPrice,
                    'delta': msg.delta,
                    'gamma': msg.gamma,
                    'vega': msg.vega,
                    'theta': msg.theta,
                    'underlying_price': msg.undPrice,
                    'pv_dividends': msg.pvDividend,
                    'implied_vol': msg.impliedVol
                })
            else:
                raise Exception("Unexpected message type: %s" % msg.typeName)
        self.connection.unregister(
            self._process_message,
            message.tickPrice,
            message.tickSnapshotEnd,
            message.tickOptionComputation
        )
        if len(opts) > 0:
            data['option'] = OptionDataQuote(opts)
        return MarketDataQuoteInstrument(instrument, data)
    
    def create_stock(self, ticker, currency='USD', exchange='SMART'):
        c = Contract()
        c.m_secType = 'STK'
        c.m_localSymbol = ticker
        c.m_currency = currency
        c.m_exchange = exchange
        return c
        
    def create_option_ticker(self, ticker, currency='USD', exchange='SMART'):
        c = Contract()
        c.m_secType = 'OPT'
        c.m_localSymbol = ticker
        c.m_currency = currency
        c.m_exchange = exchange
        return c
        
if __name__ == '__main__':
    con = Connection()
    print(con.get_current_time())
    print(con.get_positions())
