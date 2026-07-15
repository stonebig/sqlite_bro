# from pyappveyordemo.extension import some_function
import pytest
import pathlib
import tempfile

import io
from sqlite_bro import sqlite_bro
app = sqlite_bro.App()
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


def test_GridCopyFilter(monkeypatch):
    "Ctrl+c copy and Ctrl+f regex filter on a results treeview"
    from tkinter import ttk

    app.new_db(":memory:")
    tab_id = app.n.new_query_tab("Grid", "")
    app.n.add_treeview(tab_id, ("a", "b"), [(1, "Ford"), (2, "Citroën")], "t")

    def find_tree(w):
        for c in w.winfo_children():
            if isinstance(c, ttk.Treeview) and tuple(c["columns"]) == ("a", "b"):
                return c
            found = find_tree(c)
            if found is not None:
                return found

    tree = find_tree(app.tk_win)
    assert tree is not None

    # copy with no selection : header + all rows, tab-separated
    app.n.copy_rows(tree)
    assert app.tk_win.clipboard_get() == "A\tB\n1\tFord\n2\tCitroën"

    # copy a multi-selection : only those rows
    tree.selection_set(tree.get_children()[:1])
    app.n.copy_rows(tree)
    assert app.tk_win.clipboard_get() == "A\tB\n1\tFord"

    # regex filter, case-insensitive ; empty pattern restores all rows
    monkeypatch.setattr(sqlite_bro.simpledialog, "askstring",
                        lambda *a, **k: "citro")
    app.n.filter_rows(tree)
    assert len(tree.get_children()) == 1
    monkeypatch.setattr(sqlite_bro.simpledialog, "askstring",
                        lambda *a, **k: "")
    app.n.filter_rows(tree)
    assert len(tree.get_children()) == 2
    app.close_db
