"""json import / export : gui button routing, .import / .once batch, helpers"""
import json
import pathlib
import tempfile

import pytest

from sqlite_bro import sqlite_bro
from sqlite_bro.sqlite_bro import read_this_json, json_table_name, shred_query
from sqlite_bro.tests import test_general  # owner of the single gui App

app = sqlite_bro.App(use_gui=False)
needs_gui = pytest.mark.skipif(not test_general.app.use_gui, reason="no display")


def test_helpers():
    "file name to table name, and shred query proposal"
    assert json_table_name("d:/some stuff.json") == "some_stuff_raw"
    records = [{"id": 1, "the name": "bolt"}]
    query = shred_query("items_raw", records)
    assert "json_extract(json, '$.id')" in query
    assert 'json_extract(json, \'$."the name"\')' in query
    assert shred_query("t", []) == 'SELECT json FROM "t";'


def test_read_this_json():
    ".json array, single object, and .jsonl lines"
    with tempfile.TemporaryDirectory(prefix=".tmp") as tmp_dir:
        fj = str(pathlib.PurePath(tmp_dir, "t.json"))
        with open(fj, "w", encoding="utf-8") as f:
            f.write('{"solo": true}')
        assert read_this_json(fj) == [{"solo": True}]
        fl = str(pathlib.PurePath(tmp_dir, "t.jsonl"))
        with open(fl, "w", encoding="utf-8") as f:
            f.write('{"a": 1}\n\n{"a": 2}\n')
        assert read_this_json(fl) == [{"a": 1}, {"a": 2}]


def test_batch_json_import_export():
    ".import file.json + .once out.json / out.jsonl, no gui needed"
    app.new_db(":memory:")
    with tempfile.TemporaryDirectory(prefix=".tmp") as tmp_dir:
        src = str(pathlib.PurePath(tmp_dir, "items.json")).replace("\\", "/")
        with open(src, "w", encoding="utf-8") as f:
            json.dump([{"id": 1, "name": "bolt"}, {"id": 2, "name": "nut"}], f)
        out_j = str(pathlib.PurePath(tmp_dir, "out.json")).replace("\\", "/")
        out_l = str(pathlib.PurePath(tmp_dir, "out.jsonl")).replace("\\", "/")
        script = (
            '.import "%s"\n'
            ".once %s\n"
            "SELECT json_extract(json, '$.id') AS id FROM items_raw;\n"
            ".once %s\n"
            "SELECT json_extract(json, '$.name') AS name FROM items_raw;\n"
        ) % (src, out_j, out_l)
        app.n.new_query_tab("json batch", script)
        app.run_tab()
        with open(out_j, encoding="utf-8") as f:
            assert json.load(f) == [{"id": 1}, {"id": 2}]
        with open(out_l, encoding="utf-8") as f:
            assert [json.loads(l) for l in f] == [{"name": "bolt"}, {"name": "nut"}]


@needs_gui
def test_gui_json_import_opens_shred_tab():
    "the csv import button routes .json files and proposes a shred query"
    gui_app = test_general.app
    gui_app.new_db(":memory:")
    with tempfile.TemporaryDirectory(prefix=".tmp") as tmp_dir:
        src = str(pathlib.PurePath(tmp_dir, "goods.json"))
        with open(src, "w", encoding="utf-8") as f:
            json.dump([{"id": 7, "name": "screw"}], f)
        gui_app.import_csvtb(src)
        assert gui_app.conn.conn.execute(
            'SELECT count(*) FROM "goods_raw"'
        ).fetchall() == [(1,)]
        tab_id = gui_app.n.notebook.select()
        shred = gui_app.n.fw_labels[tab_id].get("1.0", "end")
        assert "json_extract" in shred and "goods_raw" in shred
