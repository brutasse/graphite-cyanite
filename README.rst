Graphite-Cyanite
================

A plugin for using graphite-web with the cassandra-based Cyanite storage
backend.

**Currently only works with @brutasse's graphite-web fork located at
https://github.com/brutasse/graphite-web/tree/feature/store-backend**.

Installation
------------

::

    pip install cyanite

Usage
-----

In your graphite's ``local_settings.py``::

    STORAGE_FINDERS = (
        'cyanite.CyaniteFinder',
    )

    CYANITE_URL = 'http://host:port'

Where ``host:port`` is the location of the Cyanite HTTP API.

See `pyr/cyanite`_ for running the Cyanite carbon daemon.

.. _pyr/cyanite: https://github.com/pyr/cyanite
