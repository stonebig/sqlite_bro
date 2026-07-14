# same scenarios as test_general_no_gui.py, but with the DuckDB engine
# (DuckDB needs typed CREATE TABLE and single-quoted string literals)
import pytest
import pathlib
import tempfile

import io

duckdb = pytest.importorskip("duckdb")
from sqlite_bro import sqlite_bro
app = sqlite_bro.App(use_gui=False)


def test_EngineDetection():
    "a .duckdb file extension must select the duckdb engine"
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        db_file = str(pathlib.PurePath(tmp_dir, 'detect.duckdb'))
        app.open_db(db_file)
        assert app.conn.engine == "duckdb"
        app.conn.close()
    app.new_db(":memory:")
    assert app.conn.engine == "sqlite"
    app.new_db(":memory:", engine="duckdb")
    assert app.conn.engine == "duckdb"


def test_Basics():
    "create script, run script, output result, check result"
    app.new_db(":memory:", engine="duckdb")
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        print(tmp_dir)
        tmp_file = str(pathlib.PurePath(tmp_dir, 'sqlite_bro_test_Basics.tmp'))
        welcome_text = """
create table item (ItemNo TEXT, Description TEXT, Kg INTEGER, PRIMARY KEY (ItemNo));
INSERT INTO item values('T','Ford',1000);
INSERT INTO item select 'A','Merced',1250 union all select 'W','Wheel',9 ;
.once %s
select ItemNo, Description, 1000*Kg Gramm  from item order by ItemNo desc;
.import %s in_this_table""" % (tmp_file, tmp_file)
        app.n.new_query_tab("Welcome", welcome_text)
        app.run_tab()
        app.close_db

        file_encoding = sqlite_bro.guess_encoding(tmp_file)[0]
        with io.open(tmp_file, mode='rt', encoding=file_encoding) as f:
            result = f.readlines()
        assert len(result) == 4
        assert result[-1] == "A,Merced,1250000\n"


def test_Outputs():
    "testing .output, .print, .header, .separator"

    app.new_db(":memory:", engine="duckdb")
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        print(tmp_dir)
        tmp_file = str(pathlib.PurePath(tmp_dir, 'sqlite_bro_test_Output.tmp'))
        welcome_text = """
create table item (ItemNo TEXT, Description TEXT, PRIMARY KEY (ItemNo));
INSERT INTO item values('DS','Citroën');
.output %s
.separator ;
.headers off
.print a;b
select * from item;
.headers on
.separator !
select * from item;
.import %s in_this_table""" % (tmp_file, tmp_file)
        app.n.new_query_tab("Welcome", welcome_text)
        app.run_tab()
        app.close_db

        file_encoding = sqlite_bro.guess_encoding(tmp_file)[0]
        with io.open(tmp_file, mode='rt', encoding=file_encoding) as f:
            result = f.readlines()
        print(result)
        assert len(result) == 4
        assert result[0] == "a;b\n"
        assert result[1] == "DS;Citroën\n"
        assert result[2] == "ItemNo!Description\n"
        assert result[3] == "DS!Citroën\n"


def test_Pydef():
    "python function embedded in sql, on the duckdb engine (needs numpy)"
    pytest.importorskip("numpy")
    app.new_db(":memory:", engine="duckdb")
    app.default_separator, app.default_header = ",", True  # reset prior state
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        tmp_file = str(pathlib.PurePath(tmp_dir, 'sqlite_bro_test_Pydef.tmp'))
        welcome_text = """
pydef py_dup(a):
    "duplicate a string"
    return a + a;
pydef py_fib(n):
   "fibonacci, annotation-less, called with an int literal"
   fib = lambda n: n if n < 2 else fib(n-1) + fib(n-2)
   return("%%s" %% fib(n*1));
pydef py_fib_t(n: int) -> int:
    "fibonacci, type-annotated : registered natively"
    fib = lambda n: n if n < 2 else fib(n-1) + fib(n-2)
    return fib(n);
.once %s
select py_dup('ab') as dup, py_fib(6) as fib, py_fib_t(7) as fib_t;""" % tmp_file
        app.n.new_query_tab("Welcome", welcome_text)
        app.run_tab()
        app.run_tab()  # re-run : pydef re-registration must not fail

        file_encoding = sqlite_bro.guess_encoding(tmp_file)[0]
        with io.open(tmp_file, mode='rt', encoding=file_encoding) as f:
            result = f.readlines()
        assert result[0] == "dup,fib,fib_t\n"
        assert result[1] == "abab,8,13\n"
        app.close_db


def test_WelcomeDemo():
    "the DuckDB welcome demo must run error-free (sql + pydef part)"
    pytest.importorskip("numpy")
    app.new_db(":memory:", engine="duckdb")
    app.output_mode, app.once_mode = False, False
    # keep only the sql + pydef part : the '.' commands part writes to ~
    demo = sqlite_bro.WELCOME_DUCKDB.split(".headers on")[0]
    # a sentinel : it is only reached if no previous instruction errored
    demo += "\ncreate table demo_ok as select 1 as ok;"
    app.n.new_query_tab("DuckDB Memo", demo)
    app.run_tab()
    assert app.conn.execute("select ok from demo_ok").fetchall() == [(1,)]
    assert app.conn.execute("select py_fib(6)").fetchall() == [('8',)]
    assert app.conn.execute("select py_fib_typed(7)").fetchall() == [(13,)]
    app.close_db


def test_Dump():
    "iterdump must produce a replayable sql script"
    app.new_db(":memory:", engine="duckdb")
    app.output_mode, app.once_mode = False, False  # reset state of prior tests
    app.n.new_query_tab(
        "Welcome",
        """create table item (ItemNo TEXT, Kg INTEGER);
INSERT INTO item values('T',1000);
create view v1 as select * from item;""",
    )
    app.run_tab()
    dump = "\n".join(app.conn.iterdump())
    assert "CREATE TABLE item" in dump
    assert "INSERT INTO \"item\" VALUES('T',1000);" in dump
    assert "CREATE VIEW v1" in dump
    app.close_db


def test_CopyPaste():
    "clipboard engines, headless: copy = export to StringIO, paste = temp csv"
    app.new_db(":memory:", engine="duckdb")
    app.output_mode, app.once_mode = False, False  # reset state of prior tests
    app.conn.execute("create table item (a INTEGER, b TEXT)")
    app.conn.execute("INSERT INTO item values (1, 'café'), (2, 'Citroën')")
    # copy engine : export_writer to a file-like target, tab-separated
    buf = io.StringIO()
    nb_columns = app.conn.export_writer(
        "select a, b from item order by a", buf, delimiter="\t")
    assert nb_columns == 2
    assert buf.getvalue() == "a\tb\r\n1\tcafé\r\n2\tCitroën\r\n"
    # the duckdb non-SELECT guard must also work with a file-like target
    assert app.conn.export_writer(
        "drop table if exists no_such_table;", io.StringIO()) == -1
    # paste engine : clipboard text written to a temp csv, guessed, imported
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        csv_file = str(pathlib.PurePath(tmp_dir, 'from_clipboard.csv'))
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            f.write(buf.getvalue())
        guess = sqlite_bro.guess_csv(csv_file)
        assert (guess.table_name, guess.default_sep, guess.has_header) == (
            "from_clipboard", "\t", True)
        sql_crea = sqlite_bro.guess_sql_creation(
            guess.table_name, guess.default_sep, ".",
            guess.has_header, guess.dlines, guess.default_quote)[0]
        reading = sqlite_bro.read_this_csv(
            csv_file, guess.encodings[0], guess.default_sep,
            guess.default_quote, guess.has_header, ".")
        app.conn.insert_reader(reading, guess.table_name, sql_crea)
        rows = app.conn.execute(
            "select * from from_clipboard order by a").fetchall()
        assert rows == [(1.0, "café"), (2.0, "Citroën")]
    app.close_db
