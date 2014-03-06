Graphite-Cyanite
================

A plugin for using graphite with the cassandra-based Cyanite storage
backend.

**Requires `Graphite-API`_ or Graphite-web 0.10.X, which are currently both
unreleased. You'll need to install from source.**

.. _Graphite-API: https://github.com/brutasse/graphite-api

Installation
------------

::

    pip install cyanite

Using with graphite-api
-----------------------

In your graphite-api config file::

    cyanite:
      url: http://cyanite-host
    finders:
      - cyanite.CyaniteFinder

Using with graphite-web
-----------------------

In your graphite's ``local_settings.py``::

    STORAGE_FINDERS = (
        'cyanite.CyaniteFinder',
    )

    CYANITE_URL = 'http://host:port'

Where ``host:port`` is the location of the Cyanite HTTP API.

See `pyr/cyanite`_ for running the Cyanite carbon daemon.

.. _pyr/cyanite: https://github.com/pyr/cyanite

Changelog
---------

* **0.2.0** (2014-03-06): Graphite-API compatibility.

* **0.1.0** (2013-12-08): initial version.
