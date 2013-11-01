#!/usr/bin/env python
# encoding: utf-8

# connection.py
# 
# Created by Maan Bsat on 2013-09-02.
# Copyright (c) 2013 Maan Bsat. All rights reserved.

from Queue import Queue
from random import randint
from datetime import datetime
import logging
import ib.opt
from ib.opt import message
from ib.ext.Contract import Contract
from untws.position import Position
from untws.market_data import *
from untws.historical_data import HistoricalDataPoint

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

    # frequencies for use with get_historical_data
    FREQ_1SEC = '1 sec'
    FREQ_5SEC = '5 secs'
    FREQ_15SEC = '15 secs'
    FREQ_30SEC = '30 secs'
    FREQ_1MIN = '1 min'
    FREQ_2MIN = '2 mins'
    FREQ_3MIN = '3 mins'
    FREQ_5MIN = '5 mins'
    FREQ_15MIN = '15 mins'
    FREQ_30MIN = '30 mins'
    FREQ_HOURLY = '1 hour'
    FREQ_DAILY = '1 day'
    
    # data types to use with get_historical_data
    HISTO_LAST = 'TRADES'
    HISTO_MID = 'MIDPOINT'
    HISTO_BID = 'BID'
    HISTO_ASK = 'ASK'
    HISTO_BID_ASK = 'BID_ASK'
    HISTO_HVOL = 'HISTORICAL_VOLATILITY'
    HISTO_IMP_VOL = 'OPTION_IMPLIED_VOLATILITY'
    
    def __init__(self, hostname, port):
        self.connection = ib.opt.ibConnection(
            host=hostname,
            port=port,
            clientId=randint(1000, 99999)
        )
        self.connection.connect()
        
        self._messages = Queue()
    
    def _process_message(self, msg):
        """Callback for ibpy"""
        logging.debug("Message received: %s" % msg.typeName)
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
    
    def get_historical_data(self, instrument, from_datetime,
        to_datetime=datetime.now(), frequency=FREQ_DAILY,
        data=HISTO_LAST, extended_hours=False):
        self.connection.register(
            self._process_message,
            message.historicalData
        )
        
        duration = int((to_datetime - from_datetime).total_seconds())
        if frequency == self.FREQ_DAILY:
            duration = '%d D' %  (duration // (60 * 60 * 24))
        else:
            duration = '%d S' % duration
        duration = '6 M'
        print('duration = "%s"' % duration)
        
        self.connection.reqHistoricalData(
            1,
            instrument,
            to_datetime.strftime('%Y%m%d %H:%M:%S'),
            duration,
            frequency,
            data,
            0 if extended_hours else 1,
            1
        )
        out = []
        while True:
            msg = self._messages.get()
            assert msg.typeName == 'historicalData'
            if msg.date.startswith('finished'):
                break
            out.append(HistoricalDataPoint(msg))
        self.connection.unregister(
            self._process_message,
            message.historicalData
        )
        return out
        
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
