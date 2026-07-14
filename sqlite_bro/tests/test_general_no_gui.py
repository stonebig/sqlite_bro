# from pyappveyordemo.extension import some_function
import pytest
import pathlib
import tempfile

import io
from sqlite_bro import sqlite_bro
app = sqlite_bro.App(use_gui=False)
def test_DeBase():
    "learning the ropes"
    assert 1 == 1


def test_Basics():
    "create script, run script, output result, check result"
    app.new_db(":memory:")
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        print(tmp_dir)
        tmp_file = str(pathlib.PurePath(tmp_dir, 'sqlite_bro_test_Basics.tmp'))
        welcome_text = """
create table item (ItemNo, Description,Kg  , PRIMARY KEY (ItemNo));
INSERT INTO item values("T","Ford",1000);
INSERT INTO item select "A","Merced",1250 union all select "W","Wheel",9 ;
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

    app.new_db(":memory:")
    with tempfile.TemporaryDirectory(prefix='.tmp') as tmp_dir:
        print(tmp_dir)
        tmp_file = str(pathlib.PurePath(tmp_dir, 'sqlite_bro_test_Output.tmp'))
        welcome_text = """
create table item (ItemNo, Description  , PRIMARY KEY (ItemNo));
INSERT INTO item values("DS","Citroën");
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


def test_CopyPaste():
    "clipboard engines, headless: copy = export to StringIO, paste = temp csv"
    app.new_db(":memory:")
    app.conn.execute("create table item (a, b)")
    app.conn.execute("INSERT INTO item values (1, 'café'), (2, 'Citroën')")
    # copy engine : export_writer to a file-like target, tab-separated
    buf = io.StringIO()
    nb_columns = app.conn.export_writer(
        "select a, b from item order by a", buf, delimiter="\t")
    assert nb_columns == 2
    assert buf.getvalue() == "a\tb\r\n1\tcafé\r\n2\tCitroën\r\n"
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
