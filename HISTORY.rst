Changelog
=========

2026-07-15 : v1.1.0 'Trust me up !'
-----------------------------------

* results grid : Ctrl+c copies the header + selected rows (or all) to the clipboard, tab-separated, no dialog

* results grid : Ctrl+f filters rows with a regular expression ; the grid title shows '(x out of N lines, filter= p)'

* publishing to PyPI is now done by GitHub Actions trusted publishing, on 'v*' tag push (no API token involved)

* fix : clicking a notebook outside the tab labels no longer raises a TclError in the console


2026-07-14 : v1.0.0 'Clip me down !'
-------------------------------------

* copy from and to the Clipboard, with 3 new toolbar icons : clipboard to table, table to clipboard, script to clipboard, 

* dialogs now pop up near the main window (multi-screen fix)

* Python-3.2 and lower version compatibility is removed, last one will be 0.14.0

* fix : the csv-sniffed quotechar was silently ignored (NameError), and export_writer now honors its quotechar parameter

* docs : icon gifs tracked in docs/output_gifs, incl. the 3 new clipboard icons, for easier maintenance


2026-07-13a : v0.14.0 'Quack me up !'
-------------------------------------

* optional DuckDB engine : create or open a '.duckdb' database (needs 'pip install duckdb'), with its own DuckDB-flavored welcome demo

* pydef embedded Python functions work on the DuckDB engine (type-annotated ones are registered natively)

* script runs now feed a single 'Logs' result tab (N°, Time, Result, Status, Instruction) : DDL/DML/pydef/dot-commands no longer spawn one result tab each, and silent statements become visible

* data grids keep their own result tabs, titled 'Qry_<n>' where <n> matches the record N° in the 'Logs' tab

* 'Logs' and 'Dump' result tabs are pinned on the left of the results notebook

* window title and database tree indicate the engine in use (SQLite or DuckDB)

* fix : refreshing the database tree no longer crashes on views repeating a column name (e.g. 'select *' over a join)


2024-05-11b : v0.13.1 'Setup me down !'
---------------------------------------

* see https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details


2024-05-11a : v0.13.0 'PEP 667 me up !'
---------------------------------------

* starting Python-3.13, PEP 667 forces us to use a specific dictionnary pydef_locals instead of locals()


2022-02-04a : v0.12.2 'Filling the blanks !'
--------------------------------------------

* empty columns names are always replaced per the default 'c_nnn' convention


2021-08-15a : v0.12.1 'Pop-up results to excel !'
-------------------------------------------------

* 'backup' and 'restore' functions are accessible via menu (for python >=3.7)

* running script and displaying output in temporary files is available via icons

* supports running in an environment with no DISPLAY


2021-08-09b : v0.11.1 'Script me more!'
---------------------------------------

* supports '.output' and '.print' functions

* supports '.dump' and '.read' functions 

* supports '.open' function

* supports '.backup' and '.restore' functions

* switch to github actions and pytest


2021-08-01a : v0.10.0 'Hello, better .scripting World!'
-------------------------------------------------------

* supports '.headers on|off' function

* supports '.separator COL' function 

* supports '.cd DIRECTORY' function

* supports command-line scripting (see sqlite_bro -h)


2021-04-25a : v0.9.3 'Hello, World!'
------------------------------------

* support functions with no parameters or parameters on several lines

2021-04-20a : v0.9.2 'Give PyPy a chance!'
------------------------------------------

* compatiblity with PyPy

* handle '~' convention for Home directory

* indicate Python Executable and Home directory in Information bubble


2019-06-16a : v0.9.1 'Support un-named Tabs!!'
----------------------------------------------

* previously, un-named Tabs couldn't be renamed nor moved.

2019-05-02a : v0.9.0 'De-duplicate column names!'
-------------------------------------------------

* header columns  in a .csv file are de-duplicated to avoid error: 'a', 'a', 'a_1' becomes 'a', 'a_2', 'a_1'

2016-03-06a : v0.8.11 'Combine Functions!'
------------------------------------------

* add a combining of functions example: 'py_func1(1*py_func2)', not 'py_func1(py_func2)' 

* fixed a nasty tokenizer issue


2015-08-12a : v0.8.10 'F9 runs !'
---------------------------------

* clicking on 'F9' key will run current selected instructions (patch by Yuxiang Wang)


2015-05-24a : v0.8.9 'Yield !'
------------------------------

* re-structure sql splitting as a generator instead of a list

* remove too long history from pypi front page


2015-04-16a : v0.8.8 'Continuous Integration !'
-------------------------------------------------

* re-structure as a package for Appveyor Continuous Integration tests

* include a global test


2014-09-10b : v0.8.7.4 '.Import this !'
---------------------------------------

* compatibility fix for python 2.7


2014-09-10a : v0.8.7.3 '.Import this !'
---------------------------------------

* wheel packaging format on pypi.org (no user code change)


2014-09-03c : v0.8.7.2 '.Import this !'
---------------------------------------

* '.once' default encoding is 'utf-8-sig' on windows


2014-09-03b : v0.8.7.1 '.Import this !'
---------------------------------------

* '.import' and '.once' support 


2014-08-09a : v0.8.6 'Committed to speed'
-----------------------------------------

* use a transaction when importing a csv file


2014-07-02b : v0.8.5 'Rename your tabs !'
-----------------------------------------

* tabs can be renamed via double-click

* more OS agnostic


2014-06-30a : v0.8.4 'Move your tabs !'
---------------------------------------

* tabs can be dragged with the mouse


2014-06-28a : v0.8.3 'Cross on tabs !'
--------------------------------------

* each tab has its closing button 

* Ctrl-Z and Ctrl-Y works on Script Text aera


2014-06-26a : v0.8.2 'Getting to the point'
-------------------------------------------

* switch to no-autocommit mode by default to allow savepoints

* a 'legacy autocommit' Open Database option is added

* add an example of COMMIT and ROLLBACK, and an example of SAVEPOINTS


2014-06-25a : v0.8.1 'Attach them all !'
----------------------------------------

* support attachement of several databases with the same name


2014-06-21a : v0.8.0 'Mark the date !'
--------------------------------------

* recognize date formats in .csv importation


2014-06-19a : v0.7.2 'Remember me'
----------------------------------

* keep memory of last directory used


2014-06-17a : v0.7.1
--------------------

* improved publishing on Pypi (was tricky, especially the front page)


2014-06-15b : v0.7.0
--------------------

* create a github project 'sqlite_bro', from 'sqlite_py_manager' baresql example

* discover how to publish on Pypi (hard)


2014-06-14c : "It's a long way to temporary !"
----------------------------------------------

* works with  temporary tables


2014-06-10a : 'Sanitizer of Python (xkcd.com/327)'
--------------------------------------------------

* imported python functions must be validated


2014-06-09a : 'The magic 8th PEP'
---------------------------------

* PEP8 alignement


2014-06-07a : 'Yield me a token'
--------------------------------

* the pythonic way to generate tokens is 'Yield'


2014-06-04a : 'Log me out !'
----------------------------

* export SQL + SQL top result in a file in 1 click


2014-06-01a 'Commit and Rollback'
---------------------------------

* support COMMIT and ROLLBACK


2014-06-03a : 'See me now ?'
----------------------------

* character INCREASE icon, so the back of the class can see


2014-05-25a : 'sql everywhere'
------------------------------

* make it work as low as Python 2.7 + SQlite 3.6.21 


2014-05-25a : 'Assassination of Class Room'
-------------------------------------------

* the GUI is a Class now


2014-05-11
----------

* addition of Tooltips over icons


2014-05-06
----------

* addition of the Welcome Demo


2014-05-01
----------

* birth : need of a ZERO-requirements SQLite Browser for a Python Class
