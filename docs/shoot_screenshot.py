"""Retake docs/sqlite_bro.GIF, the screenshot shown in README.rst.

    python docs/shoot_screenshot.py            # writes docs/sqlite_bro.GIF
    python docs/shoot_screenshot.py other.GIF  # writes somewhere else

It launches the real GUI, puts it in the state the doc shot shows (welcome
script run, the python-function line selected and run alone, database tree
open on the attached 'toto'), grabs the window and saves it as a GIF.

Windows only : the window rectangle comes from DwmGetWindowAttribute, so that
the shot holds the title bar (where the version is) without the drop shadow.
Needs Pillow, and duckdb for the second tab. Do not touch the mouse or the
keyboard while it runs : the window must keep the focus, otherwise the title
bar greys out and the script selection stops painting.
"""
import ctypes
import ctypes.wintypes
import os
import sys
import tempfile
import tkinter

from PIL import Image, ImageGrab

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlite_bro import sqlite_bro as sb  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                      os.path.join(HERE, "sqlite_bro.GIF"))
# the line the shot shows selected : it is run alone, so the result pane holds
# the two columns of a python embedded function
SEL = "select py_hello(), py_fib(6) as fibo"
# wide enough for Windows to draw the whole caption, version included : the
# caption is painted at the monitor dpi, whatever scaling Tk uses inside
GEOMETRY = "1150x660+40+40"


class Tk96(tkinter.Tk):
    """a Tk root reporting a classic 96 dpi screen

    The doc shot was taken on a 96 dpi screen. On a high-dpi one the app
    (rightly) enlarges everything, and the same window shows a third less of
    the script. Scaling Tk down keeps the layout comparable from a release to
    the next, and the window stays 1:1 with real pixels : no bitmap stretching
    by Windows, so the text of the shot stays crisp.
    """

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.tk.call("tk", "scaling", 96.0 / 72.0)


sb.Tk = Tk96

app = sb.App(use_gui=True)
app.new_db(":memory:")
tab = app.n.new_query_tab("Welcome", sb.WELCOME_TEXT)
# a DuckDB tab, as in the doc shot : opening a '.duckdb' shows the DuckDB memo,
# then we come back to the SQLite memory database the Welcome script needs
duck = os.path.join(tempfile.mkdtemp(prefix="sqlite_bro_shot"), "demo.duckdb")
app.open_db(duck)
app.open_db(":memory:")
app.n.notebook.select(tab)

win = app.tk_win
win.geometry(GEOMETRY)
win.update()


def panes():
    """the horizontal (tree | queries) pane, and the tab's script/results one"""
    horizontal = [w for w in win.winfo_children()
                  if isinstance(w, sb.ttk.Panedwindow)][0]
    vertical = app.n.fw_labels[tab].master.master
    return horizontal, vertical


def expand(tree, node="", depth=0):
    """open the database tree down to the columns of the two 'item' tables"""
    for child in tree.get_children(node):
        text = tree.item(child, "text")
        if depth < 2 or text in ("item", "new_item"):
            tree.item(child, open=True)
        if text == "new_item":
            tree.selection_set(child)
            tree.focus(child)
        expand(tree, child, depth + 1)


def stage():
    """bring the application in the state the shot shows"""
    fw = app.n.fw_labels[tab]
    app.run_tab()  # the whole script : it creates the tables and attaches toto
    start = fw.search(SEL, "1.0", stopindex="end")
    fw.tag_add("sel", start, "%s+%dc" % (start, len(SEL)))
    fw.mark_set("insert", "%s+%dc" % (start, len(SEL)))
    app.run_tab()  # then that line alone, the selection being what runs
    app.actualize_db()
    expand(app.db_tree)
    horizontal, vertical = panes()
    horizontal.sashpos(0, 200)
    vertical.sashpos(0, 400)
    # running consumed the selection : show it again, as the doc shot does
    fw.tag_add("sel", start, "%s+%dc" % (start, len(SEL)))
    fw.yview("%d.0" % (int(start.split(".")[0]) - 7))
    fw.focus_set()
    win.after(800, shoot)  # let the treeviews settle before grabbing


def shoot():
    """grab the window and save it as a GIF"""
    win.lift()
    win.focus_force()
    # a selection only paints in the widget holding the focus : give it back to
    # the script, which is where it is when a user selects and runs a line
    app.n.fw_labels[tab].focus_set()
    win.update()
    rect = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        ctypes.windll.user32.GetForegroundWindow(),
        9,  # DWMWA_EXTENDED_FRAME_BOUNDS : the visible frame, no drop shadow
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    grab = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom),
                          all_screens=True)
    # a screenshot holds few colours : 256 without dithering is near lossless
    grab.quantize(colors=256, dither=Image.Dither.NONE).save(OUT, optimize=True)
    print("saved %s %sx%s" % ((OUT,) + grab.size))
    win.destroy()  # quit as a user closing the window : mainloop then returns


win.after(400, stage)
win.mainloop()
