untws
=====

"Pythonic" access to Interactive Brokers TWS (uses IbPy)

Introduction
------------

The goal of this Python library is to provide a *well-documented*, more *Pythonic way* to access Interactive Brokers TWS. The excellent
[IbPy](https://github.com/blampe/IbPy) library already provides access to TWS,
and it mimics the Java API, which is event-driven and asynchronous. untws uses
IbPy behind the scenes to provide a more direct (i.e. synchronous) access,
which is more suitable for *scripts and other non-GUI tools*.

Requirements
------------

untws requires [IbPy](https://github.com/blampe/IbPy) (it is developed using
the latest version found on GitHub).

Quick Howto
-----------

    from untws import ib_connect
    
    # ib_connect will connect to localhost and port 7496
    # Alternatively, pass in the hostname and/or port parameters,
    # or set the IB_HOSTNAME and/or IB_PORT environment variables
    con = ib_connect()
    
    con.get_current_time()
    con.get_positions()

Todo
----

* Functionality
    * Retrieve market data
    * Create orders
* Add documentation
* Expand the Todo list