sqlite_bro : a graphic SQLite and DuckDB browser in 1 Python file
=================================================================

sqlite_bro is a tool to browse SQLite (and optionally DuckDB)
databases with any basic python installation.


Features
--------

* Tabular browsing of a SQLite or DuckDB database (needs 'pip install duckdb')

* Import/Export of .csv and .json files with auto-detection

* Import/Export of clipboard Data (copy / paste)

* Import/Export of .sql script

* Export of database creation .sql script

* Support of sql-embedded Python functions

* support supports command-line scripting if Python>=3.3 (see sqlite_bro -h), with or without Graphic User Interface

* Easy to distribute : 1 Python source file, Python and PyPy3 compatible

* Easy to start : just launch sqlite_bro

* Easy to learn : Welcome example, minimal interface

* Easy to teach : Character size, SQL + SQL result export on a click

Installation
------------

You can install, upgrade, uninstall sqlite_bro.py with these commands::

  $ apt-get install python3-tk # apt-get install python-tk if you are using python2
  $ pip install sqlite_bro
  $ pip install --upgrade sqlite_bro
  $ pip uninstall sqlite_bro

or just launch latest version from IPython with %load https://raw.githubusercontent.com/stonebig/sqlite_bro/master/sqlite_bro/sqlite_bro.py
or just copy the file 'sqlite_bro.py' to any pc and type 'python sqlite_bro.py'

Example usage 
-------------

::

  $ python -m sqlite_bro

::

  $ sqlite_bro

::

  $ sqlite_bro -h
 
Screenshots
-----------

.. image:: https://raw.githubusercontent.com/stonebig/sqlite_bro/master/docs/sqlite_bro.GIF

.. image:: https://raw.githubusercontent.com/stonebig/sqlite_bro/master/docs/sqlite_bro_command_line.GIF


Links
-----

* `Fork me on GitHub <http://github.com/stonebig/sqlite_bro>`_
