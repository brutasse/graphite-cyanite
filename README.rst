Graphite-Cyanite
================

.. image:: https://travis-ci.org/brutasse/graphite-cyanite.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/brutasse/graphite-cyanite

A plugin for using graphite with the cassandra-based Cyanite storage
backend.

Requires `Graphite-API`_ **(preferred)** or Graphite-web 0.10.X.

Graphite-API is available on PyPI. Read the `documentation`_ for more
information.

Graphite-web 0.10.X is currently unreleased. You'll need to install from
source.

.. _Graphite-API: https://github.com/brutasse/graphite-api
.. _documentation: http://graphite-api.readthedocs.org/en/latest/

Installation
------------

::

    pip install cyanite

Using with graphite-api
-----------------------

In your graphite-api config file::

    cyanite:
      urls:
        - http://cyanite-host:port
    finders:
      - cyanite.CyaniteFinder

Using with graphite-web
-----------------------

In your graphite's ``local_settings.py``::

    STORAGE_FINDERS = (
        'cyanite.CyaniteFinder',
    )

    CYANITE_URLS = (
        'http://host:port',
    )

Where ``host:port`` is the location of the Cyanite HTTP API. If you run
Cyanite on multiple hosts, specify all of them to load-balance traffic::

    # Graphite-API
    cyanite:
      urls:
        - http://host1:port
        - http://host2:port

    # Graphite-web
    CYANITE_URLS = (
        'http://host1:port',
        'http://host2:port',
    )

See `pyr/cyanite`_ for running the Cyanite carbon daemon.

.. _pyr/cyanite: https://github.com/pyr/cyanite

Changelog
---------

* **0.3.0** (2014-04-07): Change configuration syntax to allow multiple-node
  cyanite setups.

* **0.2.1** (2014-03-07): Prevent breaking graphite rendering when no data is
  returned from cyanite.

* **0.2.0** (2014-03-06): Graphite-API compatibility.

* **0.1.0** (2013-12-08): initial version.
