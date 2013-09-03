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
from position import Position

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
        self.connection.register(self._process_message, 'UpdatePortfolio', 'AccountDownloadEnd')
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
        self.connection.unregister(self._process_message, 'UpdatePortfolio', 'AccountDownloadEnd')
        return out
        
if __name__ == '__main__':
    con = Connection()
    print(con.get_current_time())
    print(con.get_positions())