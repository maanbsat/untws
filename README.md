untws
=====

"Pythonic" access to Interactive Brokers TWS (uses IbPy)

Introduction
------------

The goal of this Python library is to provide a *well-documented*, more
*Pythonic way* to access Interactive Brokers TWS. The excellent
[IbPy](https://github.com/blampe/IbPy) library already provides access to TWS,
and it mimics the Java API, which is event-driven and asynchronous. untws uses
IbPy behind the scenes to provide a more direct (i.e. synchronous) access,
which is more suitable for *scripts and other non-GUI tools*.

Requirements
------------

untws requires [IbPy](https://github.com/blampe/IbPy). Install it with:

    $ wget https://github.com/blampe/IbPy/archive/master.zip
    $ unzip master.zip
    $ cd IbPy-master/
    
    # to install it in the system libraries
    $ python setup.py.in install
    
    # to install it for the current user only:
    $ python setup.py.in install --user

> Sadly, IbPy cannot be used with pip in its current state.

Installation
------------

Install the latest untws directly with pip:

    $ pip install https://github.com/maanbsat/untws/archive/master.zip

Quick Howto
-----------

    from untws import ib_connect
    
    # ib_connect will connect to localhost and port 7496
    # Alternatively, pass in the hostname and/or port parameters,
    # or set the IB_HOSTNAME and/or IB_PORT environment variables
    con = ib_connect()
    
    con.get_current_time()
    con.get_positions()
    
    # get market data
    stk = con.create_stock('IBM')
    mkt_data = con.get_market_data(stk)
    
    # access fields directly
    mkt_data.last
    mkt_data.bid
    mkt_data.ask
    
    # same for options
    opt = con.create_option_ticker('IBM   130921P00180000')
    mkt_data = con.get_market_data(opt)

Todo
----

* Functionality
    * Retrieve hitorical data
    * Create orders
* Add documentation
* Expand the Todo list